import copy
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Self
from zoneinfo import ZoneInfo

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import BaseModel, Field, TypeAdapter
from pyproj import CRS
from shapely import Point

from ..cut_points import TRANSPORTATION_CUT_POINTS
from ..logger import generate_subject_extra
from ..logs import errors
from ..preprocessing.expanders.accelerometry import get_vector_magnitude
from ..preprocessing.expanders.spatial import (
    get_acceleration,
    get_direction,
    get_distance,
    get_speed,
)
from ..preprocessing.merging import merge_subjects
from ..preprocessing.resampling import resample
from ..preprocessing.utils.common import (
    change_timezone,
    check_correct_file_suffix,
    check_file,
    columns_checker,
    filter_by_datetime,
    fix_columns,
)
from ..preprocessing.utils.spatial import change_crs, df_to_gdf, get_crs, get_timezone
from ..processing import detect_contexts, detect_priority_contexts
from ..processing.accelerometry import (
    detect_activity_intensity_from_counts,
    detect_counts_from_raw,
    detect_wear,
)
from ..processing.spatial import (
    detect_locations,
    detect_transportation,
    detect_trips,
    get_features,
    get_location_summaries,
    get_timeline,
)
from ..visualisation.spatial import plot
from .contexts import Context, Contexts
from .metadata import Metadata
from .sample_rate import SampleRate
from .validation import Column, Schema

logger = logging.getLogger("labda")
context_parser = TypeAdapter(list[Context])


class Subject(BaseModel):
    id: str = Field(coerce_numbers_to_str=True)
    collection: str | None = None
    metadata: Metadata
    df: pd.DataFrame
    contexts: list[Context] = Field(default_factory=list)
    locations: pd.DataFrame = Field(default_factory=pd.DataFrame)

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"Subject(id={self.id}, collection={self.collection}, metadata={repr(self.metadata)}, df[shape]={self.df.shape})"

    def validate(
        self,
        *,
        extra_columns: bool = True,
    ):
        if self.df.empty:
            raise ValueError(errors["empty_dataframe"])

        self.df = Schema.validate(self.df)
        self.df = fix_columns(self.df, extra_columns)

    def to_parquet(
        self,
        path: str | Path,
        *,
        overwrite: bool = False,
        validate: bool = True,
    ) -> None:
        if isinstance(path, str):
            path = Path(path)

        check_correct_file_suffix(path, "parquet")

        if path.exists() and not overwrite:
            raise FileExistsError(
                errors["file_exists_overwrite_info"].format(path=path)
            )
        else:
            path.parent.mkdir(parents=True, exist_ok=True)

        subject_metadata = self.model_dump_json(
            exclude={"df", "contexts", "locations"}
        ).encode()  # type: ignore
        parquet_metadata = {"labda".encode(): subject_metadata}

        if validate:
            self.validate()

        table = pa.Table.from_pandas(self.df)
        existing_metadata = table.schema.metadata
        combined_meta = {**parquet_metadata, **existing_metadata}

        table = table.replace_schema_metadata(combined_meta)
        pq.write_table(table, path)

        logger.info(
            f'Subject saved to "{path}".',
            extra=generate_subject_extra(self, "structure", "subject", "to_parquet"),
        )

    @classmethod
    def from_parquet(
        cls,
        path: str | Path,
        *,
        validate: bool = True,
    ) -> Self:
        path = check_file(path, "parquet")

        df = pd.read_parquet(path, engine="fastparquet")
        metadata = pq.ParquetFile(path).metadata.metadata
        metadata = json.loads(metadata["labda".encode()])

        obj = cls.model_validate({"df": df, **metadata})

        if validate:
            obj.validate()

        logger.info(
            f'Subject loaded from "{path}".',
            extra=generate_subject_extra(obj, "structure", "subject", "from_parquet"),
        )

        return obj

    def infer_timezone(self) -> ZoneInfo:
        if not self.metadata.crs:
            raise ValueError(errors["missing_crs"])

        return get_timezone(self.df, self.metadata.crs)

    def set_timezone(
        self,
        timezone: ZoneInfo | str | None = "infer",
    ) -> None:
        source_tz = self.metadata.timezone

        if timezone is None:
            timezone = "infer"

        if isinstance(timezone, str):
            if timezone == "infer":
                timezone = self.infer_timezone()
            else:
                timezone = ZoneInfo(timezone)

        if self.metadata.timezone:
            self.df = change_timezone(self.df, self.metadata.timezone, timezone)

        self.metadata.timezone = timezone

        logger.info(
            f'Timezone changed from "{source_tz}" to "{timezone}".',
            extra=generate_subject_extra(self, "structure", "subject", "set_timezone"),
        )

    def infer_crs(self) -> CRS:
        return get_crs(self.df, self.metadata.crs)

    def set_crs(
        self,
        crs: CRS | str | None = "infer",
    ) -> None:
        source_crs = self.metadata.crs

        if (
            Column.LATITUDE not in self.df.columns
            or Column.LONGITUDE not in self.df.columns
        ):
            logger.warning(
                "Data lacks latitude and longitude information, defining a CRS is probably pointless.",
                extra=generate_subject_extra(self, "structure", "subject", "set_crs"),
            )

        if crs is None:
            crs = "infer"

        if isinstance(crs, str):
            if crs == "infer":
                crs = self.infer_crs()
            else:
                crs = CRS.from_user_input(crs)

        if self.metadata.crs:
            self.df = change_crs(self.df, self.metadata.crs, crs)

        self.metadata.crs = crs

        logger.info(
            f'CRS changed from "{source_crs}" to "{crs}".',
            extra=generate_subject_extra(self, "structure", "subject", "set_crs"),
        )

    def resample(
        self,
        target: SampleRate | timedelta | str = "uniform",
        mapper: dict[Column, Any] | None = None,
        drop: bool = False,
    ) -> None:
        source = self.metadata.sample_rate
        message = None

        if not source:
            raise ValueError(errors["missing_sample_rate"])

        if isinstance(target, SampleRate):
            pass
        elif isinstance(target, timedelta):
            target = SampleRate.from_timedelta(target)
        elif isinstance(target, str) and target == "uniform":
            target = source
        else:
            raise ValueError(errors["invalid_resample_target"].format(target=target))

        if target.value == source.value and target.unit == source.unit:
            message = f"Data aligned to {target} intervals."
        else:
            message = f"Data resampled from {source} to {target}."

        self.df, dropped_cols = resample(self.df, source, target, mapper, drop)
        self.metadata.sample_rate = target

        logger.info(
            message,
            extra=generate_subject_extra(self, "structure", "subject", "resample"),
        )

        if dropped_cols:
            dropped_cols = ", ".join([str(col) for col in dropped_cols])
            logger.warning(
                f"Columns ({dropped_cols}) were dropped during resampling.",
                extra=generate_subject_extra(self, "structure", "subject", "resample"),
            )

    def set_timeframe(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> None:
        origin_n = len(self.df)
        self.df = filter_by_datetime(self.df, start, end)
        filtered_n = len(self.df)

        logger.info(
            f"Dataset trimmed to the timeframe of {start} to {end}. {origin_n - filtered_n} data points were excluded, leaving {filtered_n} records for analysis.",
            extra=generate_subject_extra(self, "structure", "subject", "set_timeframe"),
        )

    def detect_activity_intensity_from_counts(
        self,
        cut_points: dict[str, Any],
        sensor: int | None = 0,
        overwrite: bool = False,
    ) -> None:
        name = Column.ACTIVITY_INTENSITY
        if not overwrite:
            columns_checker(self.df, [name], exists=False)

        cut_points = copy.deepcopy(cut_points)
        cut_points["sample_rate"] = SampleRate.model_validate(cut_points["sample_rate"])

        placement = self.metadata.sensors[sensor].placement if sensor else None

        self.df[name], warnings = detect_activity_intensity_from_counts(
            self.df,
            cut_points,
            self.metadata.sample_rate,
            placement,
        )

        if warnings:
            for warning in warnings:
                if warning:
                    logger.warning(
                        warning,
                        extra=generate_subject_extra(
                            self,
                            "processing",
                            "accelerometry",
                            "detect_activity_intensity_from_counts",
                        ),
                    )

    def detect_counts_from_raw(
        self,
        epoch: SampleRate | timedelta = timedelta(seconds=1),
        mapper: dict[Column, Any] | None = None,
        drop: bool = True,
        *,
        overwrite: bool = False,
    ) -> None:
        # TODO: Unify params
        counts_cols = [Column.COUNTS_X, Column.COUNTS_Y, Column.COUNTS_Z]
        if not overwrite:
            columns_checker(self.df, counts_cols, exists=False)  # type: ignore

        if isinstance(epoch, SampleRate):
            pass
        elif isinstance(epoch, timedelta):
            epoch = SampleRate.from_timedelta(epoch)

        if epoch.to_timedelta() < timedelta(seconds=1):
            raise ValueError("Epoch must be at least 1 second.")

        counts = detect_counts_from_raw(
            self.df,
            self.metadata.sample_rate,
            epoch,
        )
        counts.columns = counts_cols
        size = len(counts)
        self.resample(epoch, mapper, drop)
        counts.index = self.df[:size].index
        self.df = pd.concat([self.df[:size], counts], axis=1)
        self.df = fix_columns(self.df)
        self.metadata.sample_rate = epoch

        logger.info(
            f"Actigraph counts calculated for {epoch} intervals.",
            extra=generate_subject_extra(
                self, "processing", "accelerometry", "detect_counts_from_raw"
            ),
        )

    def merge(
        self,
        other: Self,
        how: str = "inner",
    ) -> None:
        try:
            self = merge_subjects(self, other, how)
            logger.info(
                "Subjects merged.",
                extra=generate_subject_extra(self, "preprocessing", "subject", "merge"),
            )

        except Exception as error:
            raise ValueError(errors["merge_failed"].format(error=error))

    def add_counts_vector_magnitude(
        self,
        overwrite: bool = False,
    ) -> None:
        name = Column.COUNTS_VM
        cols = [Column.COUNTS_X, Column.COUNTS_Y, Column.COUNTS_Z]

        if not overwrite:
            columns_checker(self.df, [name], exists=False)

        self.df[name] = get_vector_magnitude(self.df, cols).astype("Float32")  # type: ignore

        extra = generate_subject_extra(
            self, "processing", "accelerometry", "add_counts_vector_magnitude"
        )
        logger.info("Vector magnitude of counts calculated.", extra=extra)

    def add_distance(self, overwrite: bool = False) -> None:
        name = Column.DISTANCE
        message = "Distance calculated."

        if not overwrite:
            columns_checker(self.df, [name], exists=False)

        if not self.metadata.crs:
            raise ValueError(errors["missing_crs"])

        if self.metadata.crs == CRS.from_epsg(4326):
            message = (
                message
                + " However, CRS is WGS84 (EPSG:4326), distance calculation may not be accurate and are in degrees."
            )
            level = logging.WARNING
        else:
            level = logging.INFO

        self.df[name] = get_distance(self.df, self.metadata.crs)

        extra = generate_subject_extra(self, "processing", "spatial", "add_distance")
        logger.log(level, message, extra=extra)

    def add_speed(self, overwrite: bool = False) -> None:
        name = Column.SPEED

        if not overwrite:
            columns_checker(self.df, [name], exists=False)

        if not self.metadata.crs:
            raise ValueError(errors["missing_crs"])

        self.df[name] = get_speed(self.df, self.metadata.crs)

        extra = generate_subject_extra(self, "processing", "spatial", "add_speed")
        logger.info("Speed calculated.", extra=extra)

    def add_acceleration(self, overwrite: bool = False) -> None:
        name = Column.ACCELERATION

        if not overwrite:
            columns_checker(self.df, [name], exists=False)

        if not self.metadata.crs:
            raise ValueError(errors["missing_crs"])

        self.df[name] = get_acceleration(self.df, self.metadata.crs)

        extra = generate_subject_extra(
            self, "processing", "spatial", "add_acceleration"
        )
        logger.info("Acceleration calculated.", extra=extra)

    def add_direction(self, overwrite: bool = False) -> None:
        name = Column.DIRECTION

        if not overwrite:
            columns_checker(self.df, [name], exists=False)

        self.df[name] = get_direction(self.df)

        extra = generate_subject_extra(self, "processing", "spatial", "add_direction")
        logger.info("Direction calculated.", extra=extra)

    def detect_trips(
        self,
        gap_duration: timedelta,
        stop_radius: float,
        stop_duration: timedelta,
        pause_radius: float | None = None,
        pause_duration: timedelta | None = None,
        min_duration: timedelta | None = None,
        min_length: float | None = None,
        min_distance: float | None = None,
        indoor_limit: float | None = None,
        overwrite: bool = False,
    ) -> None:
        cols = [
            Column.SEGMENT_ID,
            Column.TRIP_STATUS,
            Column.TRIP_ID,
            Column.STATIONARY_ID,
        ]

        if not overwrite:
            columns_checker(
                self.df,
                cols,  # type: ignore
                exists=False,
            )

        if not self.metadata.crs:
            raise ValueError(errors["missing_crs"])

        self.df[cols] = detect_trips(
            self.df,
            self.metadata.sample_rate.to_timedelta(),
            self.metadata.crs,
            gap_duration,
            stop_radius,
            stop_duration,
            pause_radius,
            pause_duration,
            min_duration,
            min_length,
            min_distance,
            indoor_limit,
        )

        n_trips = self.df["trip_id"].nunique()

        extra = generate_subject_extra(self, "processing", "spatial", "detect_trips")
        logger.info(
            f"Trips detected. {n_trips} trips identified.",
            extra=extra,
        )

    def detect_transportation(
        self,
        cut_points: dict[str, Any] = TRANSPORTATION_CUT_POINTS["heidler_palms_2024"],
        window: int | None = 3,
        pause_fill: str | None = None,
        activity: bool = False,
        overwrite: bool = False,
    ) -> None:
        name = Column.TRIP_MODE

        if not self.metadata.crs:
            raise ValueError(errors["missing_crs"])

        if not overwrite:
            columns_checker(self.df, [name], exists=False)

        self.df[name] = detect_transportation(
            self.df,
            self.metadata.crs,
            cut_points,
            window,
            pause_fill,
            activity,
        )

        extra = generate_subject_extra(
            self, "processing", "spatial", "detect_transportation"
        )
        logger.info("Transportation modes detected.", extra=extra)

    def detect_wear(
        self,
        cut_points: dict[str, Any],
        sensor: int | None = 0,
        overwrite: bool = False,
    ) -> None:
        name = Column.WEAR
        if not overwrite:
            columns_checker(self.df, [name], exists=False)

        cut_points = copy.deepcopy(cut_points)
        cut_points["sample_rate"] = SampleRate.model_validate(cut_points["sample_rate"])

        placement = self.metadata.sensors[sensor].placement if sensor else None

        self.df[name], warnings = detect_wear(
            self.df,
            cut_points,
            self.metadata.sample_rate,
            placement,
        )

        if warnings:
            for warning in warnings:
                if warning:
                    logger.warning(
                        warning,
                        extra=generate_subject_extra(
                            self,
                            "processing",
                            "accelerometry",
                            "detect_wear",
                        ),
                    )

    def get_timeline(self, type: str = "trip") -> pd.DataFrame:
        if not self.metadata.crs:
            raise ValueError(errors["missing_crs"])

        match type:
            case "trip":
                timeline = get_timeline(self.df, self.metadata.crs)
            case _:
                raise ValueError(
                    errors["invalid_timeline_type"].format(
                        type=type, valid_types=", ".join(["trip"])
                    )
                )

        return timeline

    def plot(
        self,
        objects: list[str] | None = None,
        path: Path | str | None = None,
        center: Point | None = None,
        zoom: int | None = 10,
    ) -> str:
        if not self.metadata.crs:
            raise ValueError(errors["missing_crs"])

        df = self.df

        if objects and "contexts" in objects:
            contexts = self._get_context_gdf()
        else:
            contexts = pd.DataFrame()

        if objects and "locations" in objects:
            locations = self.get_locations(valid=True)
        else:
            locations = pd.DataFrame()

        return plot(
            df,
            contexts,
            locations,
            self.metadata.crs,
            objects,
            center,
            zoom,
            path,
        )

    def detect_contexts(
        self,
        contexts: Contexts,
        null: bool = False,
        priority: bool = True,
        overwrite: bool = False,
    ) -> None:
        filtered = contexts.filter(self.id, null)

        if not self.metadata.crs or not contexts.metadata.crs:
            raise ValueError(errors["missing_crs"])

        if self.contexts and not overwrite:
            raise ValueError("Contexts already detected.")

        if overwrite and "context" in self.df.columns:
            self.df.drop("context", axis=1, inplace=True)

        gdf = df_to_gdf(self.df, self.metadata.crs)
        filtered = df_to_gdf(filtered, contexts.metadata.crs, "geometry")

        results = detect_contexts(gdf, filtered)
        self.contexts = context_parser.validate_python(results)

        if priority:
            self.detect_priority_contexts()

        extra = generate_subject_extra(
            self, "processing", "contexts", "detect_contexts"
        )
        logger.info("Contexts detected.", extra=extra)

    def _get_context_gdf(self) -> pd.DataFrame:
        if not self.contexts:
            raise ValueError(errors["missing_contexts"])

        df = self.model_dump(
            include={"contexts"},
            exclude={"contexts": {"__all__": "indexes"}},  # type: ignore
        ).get("contexts")

        return pd.DataFrame(df)  # type: ignore

    def detect_priority_contexts(
        self,
        overwrite: bool = False,
    ) -> None:
        name = Column.CONTEXT
        if not overwrite:
            columns_checker(self.df, [name], exists=False)

        self.df[name] = detect_priority_contexts(self.df, self.contexts)

        extra = generate_subject_extra(
            self, "processing", "contexts", "detect_priority_contexts"
        )
        logger.info("Priority context detected.", extra=extra)

    def detect_locations(
        self,
        features: pd.DataFrame,
        duration: timedelta | None = None,
        locations_buffer: float = 10,
        limit: float | None = 0.8,
        overwrite: bool = False,
    ) -> None:
        df = self.df
        crs = self.metadata.crs

        if not self.locations.empty and not overwrite:
            raise ValueError("Locations already detected.")

        if not crs:
            raise ValueError(errors["missing_crs"])

        self.locations = detect_locations(
            df, features, crs, duration, limit, locations_buffer
        )

    def get_locations(
        self,
        valid: bool = False,
    ) -> pd.DataFrame:
        if not self.metadata.crs:
            raise ValueError(errors["missing_crs"])

        if self.locations.empty:
            raise ValueError("Locations not detected.")

        summaries = get_location_summaries(self.locations, self.metadata.crs, valid)

        return summaries
