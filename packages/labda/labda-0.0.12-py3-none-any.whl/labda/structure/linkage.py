import logging
from pathlib import Path
from typing import Any, Self
from zoneinfo import ZoneInfo

import pandas as pd
from pydantic import BaseModel, Field
from pyproj import CRS

from ..logger import generate_extra
from ..logs import errors
from ..preprocessing.utils.common import check_file, check_size, normalize_column_names
from .metadata import BaseMetadata
from .validation import LinkageColumn, LinkageSchema

logger = logging.getLogger("labda")


def _parse_linkage(
    df: pd.DataFrame,
    format: str | None = None,
) -> pd.DataFrame:
    normalize_column_names(df)
    check_size(df, None)

    if LinkageColumn.START in df.columns:
        df[LinkageColumn.START] = pd.to_datetime(df[LinkageColumn.START], format=format)

    if LinkageColumn.END in df.columns:
        df[LinkageColumn.END] = pd.to_datetime(df[LinkageColumn.END], format=format)

    df = LinkageSchema.validate(df)

    return df


class Linkage(BaseModel):
    # TODO: Lot of duplication for classmethod from_csv and from_excel. Rework it.
    id: str = Field(coerce_numbers_to_str=True)
    metadata: BaseMetadata
    df: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_excel(
        cls,
        path: Path | str,
        id: str | None = None,
        timezone: ZoneInfo | None = None,
        crs: CRS | None = None,
        validate: bool = True,
    ) -> pd.DataFrame:
        path = check_file(path, "xlsx")
        df = pd.read_excel(path)
        df = _parse_linkage(df)

        metadata = BaseMetadata(timezone=timezone, crs=crs)

        if not id:
            id = f"{path.stem}[temporary name]"

        obj = cls(id=id, metadata=metadata, df=df)

        if validate:
            obj.validate()

        logger.info(
            f'Linkage loaded from "{path.as_posix()}".',
            extra=generate_extra(None, "other", "preprocessing", "linkage", "from_csv"),
        )

        return df

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
        df = _parse_linkage(df, format=datetime_format)

        metadata = BaseMetadata(timezone=timezone, crs=crs)

        if not id:
            id = f"{path.stem}[temporary name]"

        obj = cls(id=id, metadata=metadata, df=df)

        if validate:
            obj.validate()

        logger.info(
            f'Linkage loaded from "{path.as_posix()}".',
            extra=generate_extra(None, "other", "preprocessing", "linkage", "from_csv"),
        )

        return obj

    def validate(
        self,
        # extra_columns: bool = True,
    ):
        if self.df.empty:
            raise ValueError(errors["empty_dataframe"])

        self.df = LinkageSchema.validate(self.df)
        # TODO: Fix the columns order so it is always as prescribed in the schema. Look for fix_columns func in utils.common, then make available extra_columns parameter.

    def filter(
        self,
        subject_id: str,
        null: bool = False,
    ) -> pd.DataFrame:
        rules = self.df[LinkageColumn.SUBJECT_ID] == subject_id

        if null:
            rules = rules | (self.df[LinkageColumn.SUBJECT_ID].isna())

        df = self.df.loc[rules]

        if df.empty:
            raise ValueError("No values found for subject.")

        return df
