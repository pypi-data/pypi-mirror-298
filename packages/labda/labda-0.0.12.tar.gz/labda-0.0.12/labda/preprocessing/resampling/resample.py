from datetime import timedelta
from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from ...structure import SampleRate

from ...structure.validation import Column
from .downsample import DOWNSAMPLE
from .uniform import UNIFORM


def _determine_mapper(
    source_sec: timedelta,
    target_sec: timedelta,
    mapper: dict[Column, Any] | None,
) -> dict[Column, Any]:
    if mapper:
        return mapper

    if source_sec < target_sec:
        return DOWNSAMPLE
    elif source_sec > target_sec:
        raise ValueError(f"Upsampling is not supported ({source_sec} < {target_sec}).")
    else:
        return UNIFORM


def _validate_columns(
    df: pd.DataFrame,
    mapper: dict[Column, Any],
    drop: bool,
) -> tuple[dict[Column, Any], list[Column | str]]:
    columns = list(mapper.keys())

    dropped = [col for col in df.columns if col not in columns]

    if not drop and dropped:
        raise ValueError(f"Columns {dropped} are missing in mapper.")

    mapper = {col: method for col, method in mapper.items() if col in df.columns}

    return mapper, dropped


def resample(
    df: pd.DataFrame,
    source: "SampleRate",
    target: "SampleRate",
    mapper: dict[Column, Any] | None = None,
    drop: bool = False,
) -> tuple[pd.DataFrame, list[Column | str]]:
    source_sec = source.to_timedelta()
    target_sec = target.to_timedelta()

    mapper = _determine_mapper(source_sec, target_sec, mapper)
    mapper, dropped = _validate_columns(df, mapper, drop)

    df = df.resample(target_sec).agg(mapper)  # type: ignore
    df.dropna(inplace=True, how="all")

    return df, dropped
