import logging
import multiprocessing as mp
import secrets
from datetime import timedelta
from functools import partial
from pathlib import Path
from typing import Any, Callable, Self
from zoneinfo import ZoneInfo

import pandas as pd
from pydantic import BaseModel, Field, model_validator
from pyproj import CRS

from ..cut_points import TRANSPORTATION_CUT_POINTS
from ..logger import generate_collection_extra
from ..preprocessing.merging import merge_collections
from ..preprocessing.utils.common import get_most_frequent_value

# from ..settings import settings
from .linkage import Linkage
from .sample_rate import SampleRate
from .subject import Subject
from .validation import Column

logger = logging.getLogger("labda")


def _handle_logs(
    stats: dict[str, int], messages: dict[str, str], extra: dict[str, Any]
):
    if stats["success"] == 0:
        raise ValueError(messages["error"])
    elif stats["failed"] == 0:
        level = logging.INFO
        msg = messages["success"]
    else:
        level = logging.WARNING
        msg = messages["warning"]

    logger.log(level, msg, extra=extra)


def _process_sbj(
    subject: Subject | Path,
    func: Callable,
    extra: dict[str, Any],
    linkage: tuple[Linkage, list[str]] | None,
    nullable: bool,
    **kwargs,
) -> tuple[bool, None | Subject | Any]:
    try:
        if isinstance(subject, Subject) and linkage:
            sbj_args = linkage[0].filter(subject.id, linkage[1], nullable)
            kwargs = {**kwargs, **sbj_args}

        res = func(subject, **kwargs)

        return True, res or subject

    except Exception as e:
        if isinstance(subject, Path):
            extra["subject"] = subject.name
        else:
            extra["subject"] = subject.id
        logger.error(e, extra=extra)

        return False, subject


def _parallel_processing(
    func: Callable,
    subjects: list[Subject | Path],
    extra: dict[str, Any],
    linkage: tuple[Linkage, list[str]] | None = None,
    nullable: bool = False,
    **kwargs,
) -> tuple[list[Subject | Any | None], dict[str, int]]:
    n_cores = mp.cpu_count()

    with mp.Pool(n_cores) as pool:
        results = pool.map(
            partial(
                _process_sbj,
                func=func,
                extra=extra,
                linkage=linkage,
                nullable=nullable,
                **kwargs,
            ),
            subjects,
        )

    results = [res[1] for res in results if res[0]]
    stats = {
        "success": len(results),
        "failed": len(subjects) - len(results),
        "total": len(subjects),
    }
    # TODO: Change it, so user can have access to failed subjects.
    # TODO: Always should be returned all subjects, even the failed ones, so user can do something with them.
    # TODO: Remove "total" from stats, it's not necessary. Logs should then be able to handle it.

    return results, stats


def _to_parquet_with_path(
    subject: Subject,
    path: Path,
    overwrite: bool,
    validate: bool,
) -> None:
    subject_path = path / f"{subject.id}.parquet"
    return Subject.to_parquet(
        subject, path=subject_path, overwrite=overwrite, validate=validate
    )


class Collection(BaseModel):
    id: str | None = Field(
        default_factory=lambda: secrets.token_hex(4), coerce_numbers_to_str=True
    )
    subjects: list[Subject] = Field(default_factory=list)

    class Config:
        validate_assignment = True

    @model_validator(mode="after")
    def propagate_id_change(self) -> Self:
        for subject in self.subjects:
            subject.collection = self.id

        return self

    def __repr__(self):
        subjects = ", ".join([sbj.id for sbj in self.subjects])  # type: ignore
        return f"Collection(id={self.id}, subjects=[{subjects}])"

    def add_subject(self, subject: Subject):
        subjects_ids = [s.id for s in self.subjects]

        if subject.id in subjects_ids:
            raise ValueError(
                f'Subject with id "{subject.id}" already exists in collection.'
            )

        subject.collection = self.id
        self.subjects.append(subject)

    def get_subject(self, id: str) -> Subject:
        for subject in self.subjects:
            if subject.id == id:
                return subject
        raise ValueError(f'Subject with id "{id}" not found.')

    @classmethod
    def from_folder(
        cls,
        path: str | Path,
        *,
        validate: bool = True,
    ) -> "Collection":
        if isinstance(path, str):
            path = Path(path)

        if not path.is_dir():
            raise ValueError(f'"{path}" is not a valid directory.')

        files = list(path.glob("*.parquet"))

        if not files:
            raise ValueError(f'No parquet files found in "{path}".')

        collection = cls(id=f"{path.name}[temporary name]")
        extra = generate_collection_extra(
            collection, "structure", "collection", "from_folder"
        )

        collection.subjects, stats = _parallel_processing(  # type: ignore
            Subject.from_parquet,
            files,  # type: ignore
            extra=extra,
            validate=validate,
        )

        if not collection.subjects:
            raise ValueError(f'No subjects loaded from "{path}".')

        collection_id = list(set([sbj.collection for sbj in collection.subjects]))  # type: ignore
        if len(collection_id) > 1:
            raise ValueError(
                f"Multiple collections found in the same folder: {', '.join(collection_id)}"  # type: ignore
            )
        elif len(collection_id) == 1:
            id = collection_id[0]

        collection.id = id
        extra["id"] = id

        if stats["failed"] == 0:
            logger.info(
                f'All ({stats["total"]}) subjects loaded successfully from "{path}".',
                extra=extra,
            )
        else:
            logger.warning(
                f'{stats["success"]} of {stats["total"]} ({stats["failed"]} failed) subjects loaded successfully from "{path}".',
                extra=extra,
            )

        return collection

    def to_folder(
        self,
        path: str | Path,
        *,
        overwrite: bool = False,
        validate: bool = True,
    ):
        if isinstance(path, str):
            path = Path(path)

        path.mkdir(parents=True, exist_ok=True)

        if not path.is_dir():
            raise ValueError(f'"{path}" is not a valid directory.')

        extra = generate_collection_extra(self, "structure", "collection", "to_folder")

        _, stats = _parallel_processing(
            partial(
                _to_parquet_with_path,
                path=path,
                overwrite=overwrite,
                validate=validate,
            ),
            self.subjects,  # type: ignore
            extra=extra,
        )

        _handle_logs(
            stats,
            {
                "success": f'All ({stats["total"]}) subjects saved to "{path}".',
                "warning": f'{stats["success"]} of {stats["total"]} ({stats["failed"]} failed) subjects saved to "{path}".',
                "error": f'No subjects saved to "{path}".',
            },
            extra,
        )

    def set_timezone(
        self,
        timezone: ZoneInfo | str | None = "infer",
    ) -> None:
        extra = generate_collection_extra(
            self, "structure", "collection", "set_timezone"
        )

        if timezone is None:
            timezone = "infer"

        if isinstance(timezone, str) and timezone == "infer":
            timezones, stats = _parallel_processing(
                Subject.infer_timezone,
                self.subjects,  # type: ignore
                extra=extra,
            )  # type: list[ZoneInfo] # type: ignore

            uniques = list(set(timezones))
            if len(uniques) == 1:
                timezone = uniques[0]  # type: ignore
            else:
                timezone = get_most_frequent_value(timezones)
                timezone = ZoneInfo(timezone)  # type: ignore

        self.subjects, stats = _parallel_processing(  # type: ignore
            Subject.set_timezone,
            self.subjects,  # type: ignore
            extra=extra,
            timezone=timezone,
        )

        _handle_logs(
            stats,
            {
                "success": f'Timezone "{timezone}" was set for all ({stats["total"]}) subjects.',
                "warning": f'Timezone "{timezone}" was set for {stats["success"]} of {stats["total"]} subjects ({stats["failed"]} failed).',
                "error": f'Timezone "{timezone}" was not set for any of the subjects ({stats["total"]}).',
            },
            extra,
        )

    def set_crs(
        self,
        crs: CRS | str | None = "infer",
    ) -> None:
        extra = generate_collection_extra(self, "structure", "collection", "set_crs")

        if crs is None:
            crs = "infer"

        if isinstance(crs, str) and crs == "infer":
            systems, stats = _parallel_processing(
                Subject.infer_crs,
                self.subjects,  # type: ignore
                extra=generate_collection_extra(
                    self, "structure", "collection", "set_crs"
                ),
            )  # type: list[CRS] # type: ignore

            uniques = list(set(systems))
            if len(uniques) == 1:
                crs = uniques[0]  # type: ignore
            else:
                crs = get_most_frequent_value(systems)
                crs = CRS.from_user_input(crs)

        self.subjects, stats = _parallel_processing(  # type: ignore
            Subject.set_crs,
            self.subjects,  # type: ignore
            crs=crs,
            extra=extra,
        )

        _handle_logs(
            stats,
            {
                "success": f'CRS "{crs}" was set for all ({stats["total"]}) subjects.',
                "warning": f'CRS "{crs}" was set for {stats["success"]} of {stats["total"]} subjects ({stats["failed"]} failed).',
                "error": f'CRS "{crs}" was not set for any of the subjects ({stats["total"]}).',
            },
            extra,
        )

    def resample(
        self,
        target: SampleRate | timedelta | str = "uniform",
        mapper: dict[Column, Any] | None = None,
        drop: bool = False,
    ) -> None:
        extra = generate_collection_extra(self, "structure", "collection", "resample")

        if isinstance(target, str) and target == "uniform":
            sample_rates = [
                subject.metadata.sample_rate.to_timedelta() for subject in self.subjects
            ]

            uniques = list(set(sample_rates))
            if len(uniques) == 1:
                target = SampleRate.from_timedelta(uniques[0])
            else:
                target = get_most_frequent_value(sample_rates)
                target = SampleRate.from_timedelta(target)  # type: ignore

        self.subjects, stats = _parallel_processing(  # type: ignore
            Subject.resample,
            self.subjects,  # type: ignore
            target=target,
            mapper=mapper,
            drop=drop,
            extra=extra,
        )

        _handle_logs(
            stats,
            {
                "success": f'Sample rate "{target}" was set for all ({stats["total"]}) subjects.',
                "warning": f'Sample rate "{target}" was set for {stats["success"]} of {stats["total"]} subjects ({stats["failed"]} failed).',
                "error": f'Sample rate "{target}" was not set for any of the subjects ({stats["total"]}).',
            },
            extra,
        )

    def _atribute_consistency_check(
        self, metadata: pd.DataFrame, attribute: str
    ) -> bool:
        unique = metadata[attribute].unique()

        if len(unique) != 1:
            unique = ", ".join(unique.tolist())

            logger.warning(
                f"Inconsistency [{attribute}]: {unique}",
                extra=generate_collection_extra(
                    self, "structure", "collection", "consistency"
                ),
            )

            return False
        else:
            return True

    def consistency(self) -> tuple[bool, pd.DataFrame | None]:
        # TODO: Add also check columns consistency
        metadatas = []
        for sbj in self.subjects:
            metadatas.append(
                {
                    "id": str(sbj.id),
                    "sample_rate": str(sbj.metadata.sample_rate),
                    "timezone": str(sbj.metadata.timezone),
                    "crs": str(sbj.metadata.crs),
                }
            )

        metadata = metadatas[0]
        metadatas = pd.DataFrame(metadatas)
        metadatas.set_index("id", inplace=True)

        consistency_results = [
            self._atribute_consistency_check(metadatas, attr)
            for attr in ["sample_rate", "crs", "timezone"]
        ]

        if all(consistency_results):
            metadata = (
                f'SR: {metadata["sample_rate"]}',
                f'TZ: {metadata["timezone"]}',
                f'CRS: {metadata["crs"]}',
            )
            logger.info(
                f'Consistency check passed ({", ".join(metadata)}).',
                extra=generate_collection_extra(
                    self, "structure", "collection", "consistency"
                ),
            )

            return True, None
        else:
            return False, metadatas

    def validate(
        self,
        extra_columns: bool = True,
    ) -> None:
        extra = generate_collection_extra(self, "structure", "collection", "validate")

        _parallel_processing(
            Subject.validate,
            self.subjects,  # type: ignore
            extra=extra,
            extra_columns=extra_columns,
        )

    def merge(
        self,
        other: Self,
        how: str = "inner",
    ) -> None:
        # TODO Add support for parallel merge.
        # TODO: Fix logging for specific number of failed subjects.
        extra = generate_collection_extra(self, "structure", "collection", "validate")

        self, failed = merge_collections(self, other, how)

        if failed:
            logger.error(
                f"Not all subjects were merged. {failed} subjects failed.",
                extra=extra,
            )
        else:
            logger.info(
                "Collections merged.",
                extra=extra,
            )

    def set_timeframe(
        self,
        start: pd.Timestamp | None = None,
        end: pd.Timestamp | None = None,
        linkage: Linkage | None = None,
    ) -> None:
        extra = generate_collection_extra(
            self, "structure", "collection", "set_timeframe"
        )

        linkage_args = ["start", "end"]

        self.subjects, stats = _parallel_processing(  # type: ignore
            Subject.set_timeframe,
            self.subjects,  # type: ignore
            start=start,
            end=end,
            extra=extra,
            linkage=(linkage, linkage_args) if linkage else None,
        )

        _handle_logs(
            stats,
            {
                "success": f'Timeframes were set for all ({stats["total"]}) subjects.',
                "warning": f'Timeframes were set for {stats["success"]} of {stats["total"]} subjects ({stats["failed"]} failed).',
                "error": f'Timeframes were not set for any of the subjects ({stats["total"]}).',
            },
            extra,
        )

    def detect_activity_intensity_from_counts(
        self,
        cut_points: dict[str, Any],
        sensor: int | None = 0,
        overwrite: bool = False,
    ) -> None:
        extra = generate_collection_extra(
            self, "structure", "collection", "detect_activity_intensity_from_counts"
        )

        self.subjects, stats = _parallel_processing(  # type: ignore
            Subject.detect_activity_intensity_from_counts,
            self.subjects,  # type: ignore
            extra=extra,
            cut_points=cut_points,
            sensor=sensor,
            overwrite=overwrite,
        )

        _handle_logs(
            stats,
            {
                "success": f'Activity intensity was detected for all ({stats["total"]}) subjects.',
                "warning": f'Activity intensity was detected for {stats["success"]} of {stats["total"]} subjects ({stats["failed"]} failed).',
                "error": f'Activity intensity was not detected for any of the subjects ({stats["total"]}).',
            },
            extra,
        )

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
        extra = generate_collection_extra(
            self, "structure", "collection", "detect_trips"
        )

        self.subjects, stats = _parallel_processing(  # type: ignore
            Subject.detect_trips,
            self.subjects,  # type: ignore
            extra=extra,
            gap_duration=gap_duration,
            stop_radius=stop_radius,
            stop_duration=stop_duration,
            pause_radius=pause_radius,
            pause_duration=pause_duration,
            min_duration=min_duration,
            min_length=min_length,
            min_distance=min_distance,
            indoor_limit=indoor_limit,
            overwrite=overwrite,
        )

        _handle_logs(
            stats,
            {
                "success": f'Trips were detected for all ({stats["total"]}) subjects.',
                "warning": f'Trips were detected for {stats["success"]} of {stats["total"]} subjects ({stats["failed"]} failed).',
                "error": f'Trips were not detected for any of the subjects ({stats["total"]}).',
            },
            extra,
        )

    def detect_transportation(
        self,
        cut_points: dict[str, Any] = TRANSPORTATION_CUT_POINTS["heidler_palms_2024"],
        window: int | None = 3,
        pause_fill: str | None = None,
        activity: bool = False,
        overwrite: bool = False,
    ) -> None:
        extra = generate_collection_extra(
            self, "structure", "collection", "detect_transportation"
        )

        self.subjects, stats = _parallel_processing(  # type: ignore
            Subject.detect_transportation,
            self.subjects,  # type: ignore
            extra=extra,
            cut_points=cut_points,
            window=window,
            pause_fill=pause_fill,
            activity=activity,
            overwrite=overwrite,
        )

        _handle_logs(
            stats,
            {
                "success": f'Transportation was detected for all ({stats["total"]}) subjects.',
                "warning": f'Transportation was detected for {stats["success"]} of {stats["total"]} subjects ({stats["failed"]} failed).',
                "error": f'Transportation was not detected for any of the subjects ({stats["total"]}).',
            },
            extra,
        )
