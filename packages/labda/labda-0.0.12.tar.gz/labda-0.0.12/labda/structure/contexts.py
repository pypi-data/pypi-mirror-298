import logging
from datetime import datetime, time
from pathlib import Path
from typing import Self
from zoneinfo import ZoneInfo

import geopandas as gpd
import pandas as pd
import shapely
from pydantic import BaseModel, Field
from pyproj import CRS

from ..logger import generate_extra
from ..logs import errors
from ..preprocessing.utils.common import (
    change_timezone,
    check_file,
    check_size,
    columns_checker,
    normalize_column_names,
)
from ..preprocessing.utils.spatial import change_crs, gdf_to_df, get_crs, get_timezone
from .metadata import BaseMetadata
from .validation import ContextsColumn, ContextsSchema

logger = logging.getLogger("labda")


def _parse_contexts(
    df: pd.DataFrame,
    format: str | None = None,
) -> pd.DataFrame:
    normalize_column_names(df)
    check_size(df, None)

    if ContextsColumn.START in df.columns:
        df[ContextsColumn.START] = pd.to_datetime(
            df[ContextsColumn.START], format=format
        )

    if ContextsColumn.END in df.columns:
        df[ContextsColumn.END] = pd.to_datetime(df[ContextsColumn.END], format=format)

    df = ContextsSchema.validate(df)

    return df


class Contexts(BaseModel):
    id: str = Field(coerce_numbers_to_str=True)
    metadata: BaseMetadata
    df: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_csv(
        cls,
        path: Path | str,
        id: str | None = None,
        timezone: ZoneInfo | None = None,
        crs: CRS | None = None,
        datetime_format: str = "%Y-%m-%d %H:%M:%S",
        validate: bool = True,
    ) -> Self:
        path = check_file(path, "csv")
        df = pd.read_csv(path, engine="pyarrow")
        df = _parse_contexts(df, format=datetime_format)

        metadata = BaseMetadata(timezone=timezone, crs=crs)

        if not id:
            id = f"{path.stem}[temporary name]"

        obj = cls(id=id, metadata=metadata, df=df)

        if validate:
            obj.validate()

        logger.info(
            f'Contexts loaded from "{path.as_posix()}".',
            extra=generate_extra(
                None, "other", "preprocessing", "contexts", "from_csv"
            ),
        )

        return obj

    @classmethod
    def from_geojson(
        cls,
        path: Path | str,
        id: str | None = None,
        timezone: ZoneInfo | None = None,
        datetime_format: str = "%Y-%m-%d %H:%M:%S",
        validate: bool = True,
    ) -> Self:
        path = check_file(path, "geojson")
        gdf = gpd.read_file(path)
        df = gdf_to_df(gdf, ContextsColumn.GEOMETRY)
        df = _parse_contexts(df, format=datetime_format)

        if "start" not in df.columns:
            df["start"] = pd.NaT

        if "end" not in df.columns:
            df["end"] = pd.NaT

        metadata = BaseMetadata(timezone=timezone, crs=gdf.crs)

        if not id:
            id = f"{path.stem}[temporary name]"

        obj = cls(id=id, metadata=metadata, df=df)

        if validate:
            obj.validate()

        logger.info(
            f'Contexts loaded from "{path.as_posix()}".',
            extra=generate_extra(
                None, "other", "preprocessing", "contexts", "from_geojson"
            ),
        )

        return obj

    def validate(
        self,
        # extra_columns: bool = True,
    ):
        if self.df.empty:
            raise ValueError(errors["empty_dataframe"])

        self.df = ContextsSchema.validate(self.df)
        # TODO: Fix the columns order so it is always as prescribed in the schema. Look for fix_columns func in utils.common, then make available extra_columns parameter.

    def infer_crs(self) -> CRS:
        return get_crs(self.df, self.metadata.crs, ContextsColumn.GEOMETRY)

    def set_crs(
        self,
        crs: CRS | str | None = "infer",
    ) -> None:
        source_crs = self.metadata.crs

        if ContextsColumn.GEOMETRY not in self.df.columns:
            logger.warning(
                "Data lacks geometry information, defining a CRS is probably pointless.",
                extra=generate_extra(None, "other", "structure", "contexts", "set_crs"),
            )

        if crs is None:
            crs = "infer"

        if isinstance(crs, str):
            if crs == "infer":
                crs = self.infer_crs()
            else:
                crs = CRS.from_user_input(crs)

        self.df = change_crs(self.df, source_crs, crs, ContextsColumn.GEOMETRY)  # type: ignore
        self.metadata.crs = crs

        logger.info(
            f'CRS changed from "{source_crs}" to "{crs}".',
            extra=generate_extra(None, "other", "structure", "contexts", "set_crs"),
        )

    def infer_timezone(self) -> ZoneInfo:
        if not self.metadata.crs:
            raise ValueError(errors["missing_crs"])

        return get_timezone(
            self.df, self.metadata.crs, geometry=ContextsColumn.GEOMETRY
        )

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
            extra=generate_extra(
                None, "other", "structure", "contexts", "set_timezone"
            ),
        )

    def filter(
        self,
        subject_id: str,
        null: bool = False,
    ) -> pd.DataFrame:
        columns_checker(self.df, [ContextsColumn.SUBJECT_ID], True)

        rules = self.df[ContextsColumn.SUBJECT_ID] == subject_id

        if null:
            rules = rules | (self.df[ContextsColumn.SUBJECT_ID].isna())

        df = self.df.loc[rules]

        if df.empty:
            raise ValueError("No values found for subject.")

        return df


class Context(BaseModel):
    name: str = Field(validation_alias="context")
    priority: int
    start: datetime | time | None = None
    end: datetime | time | None = None
    geometry: shapely.geometry.base.BaseGeometry | None = None
    indexes: pd.DatetimeIndex

    class Config:
        arbitrary_types_allowed = True
