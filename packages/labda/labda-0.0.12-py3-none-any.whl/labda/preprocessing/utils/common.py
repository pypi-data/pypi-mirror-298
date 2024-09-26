import secrets
import string
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from ...logs import errors
from ...structure.validation import Column
from ..expanders.common import get_timedelta

DEFAULT_TIMEZONE = ZoneInfo("UTC")


def check_correct_file_suffix(
    path: Path,
    suffix: str,
):
    if path.suffix.lstrip(".").lower() != suffix:
        raise FileNotFoundError(errors["file_suffix"].format(path=path))


def check_size(
    df: pd.DataFrame,
    min_rows: int | None = 10,
) -> None:
    if df.empty:
        raise ValueError(errors["empty_dataframe"])

    if min_rows and len(df) < min_rows:
        raise ValueError(errors["few_dataframe_rows"].format(min_rows))


def check_file(
    path: Path | str,
    suffix: str,
):
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise FileNotFoundError(errors["path_doesnt_exist"].format(path=path))

    if not path.is_file():
        raise FileNotFoundError(errors["not_a_file"].format(path=path))

    check_correct_file_suffix(path, suffix)

    return path


def extract_id(path) -> str:
    return path.stem


def columns_checker(
    df: pd.DataFrame,
    columns: list[Column | str],
    exists: bool,
) -> None:
    if exists:
        missing_columns = [col for col in columns if col not in df.columns]

        if missing_columns:
            missing_columns = ", ".join(missing_columns)
            raise ValueError(
                errors["columns_not_exists"].format(missing_columns=missing_columns)
            )
    else:
        existing_columns = [col for col in columns if col in df.columns]

        if existing_columns:
            existing_columns = ", ".join(existing_columns)
            raise ValueError(
                errors["columns_exists"].format(existing_columns=existing_columns)
            )


def columns_exists(
    df: pd.DataFrame,
    columns: list[Column | str],
) -> None:
    """
    Checks if the given columns exist in the DataFrame.

    This function iterates over the list of columns and checks if each column exists in the DataFrame.
    If a column does not exist, it raises a ValueError.

    Args:
        df (pd.DataFrame): The DataFrame to check.
        columns (list[str]): A list of column names to check for existence in the DataFrame.

    Raises:
        ValueError: If a column does not exist in df.
    """

    missing_columns = [col for col in columns if col not in df.columns]

    if missing_columns:
        missing_columns = ", ".join(missing_columns)
        raise ValueError(
            errors["columns_not_exists"].format(missing_columns=missing_columns)
        )


def columns_not_exists(
    df: pd.DataFrame,
    columns: list[Column | str],
    *,
    overwrite: bool = False,
) -> None:
    """
    Checks if the specified columns do not exist in the DataFrame. If 'overwrite' is True,
    existing columns will be dropped. If 'overwrite' is False, an error will be raised for existing columns.

    Args:
        df (pd.DataFrame): The DataFrame to check.
        columns (List[str]): A list of column names to check.
        overwrite (bool, optional): Whether to drop existing columns. Defaults to False.

    Raises:
        ValueError: If 'overwrite' is False and any of the specified columns exist in the DataFrame.

    Returns:
        None
    """
    existing_columns = [col for col in columns if col in df.columns]

    if existing_columns:
        if overwrite:
            df.drop(columns=existing_columns, inplace=True)
        else:
            existing_columns = ", ".join(existing_columns)
            raise ValueError(
                errors["columns_exists"].format(existing_columns=existing_columns)
            )


def get_consecutive_samples(
    df: pd.DataFrame,
    n: int,
) -> pd.DataFrame:
    if n < len(df):
        # Generate a random starting index
        start_idx = np.random.randint(0, len(df) - n + 1)

        # Slice the DataFrame to get n consecutive rows
        sampled_df = df.iloc[start_idx : start_idx + n]
    else:
        sampled_df = df

    return sampled_df


def get_sampling_rate(
    df: pd.DataFrame,
    sample: int = 1000,
    limit: float = 0.7,
    tolerance: float = 0.05,
) -> dict[str, Any]:
    df = get_consecutive_samples(df, sample)

    sample_rates = get_timedelta(df).value_counts()
    sample_rate = sample_rates.idxmax().total_seconds()  # type:ignore

    sample_rates = sample_rates.to_frame("count")
    sample_rates["seconds"] = sample_rates.index.total_seconds()  # type:ignore
    sample_rates["tolerance"] = np.isclose(
        sample_rate, sample_rates["seconds"], rtol=tolerance
    )

    n = len(df)
    count = sample_rates.loc[sample_rates["tolerance"], "count"]
    percentage = count.sum() / n

    if percentage < limit:
        raise ValueError(
            errors["sample_rate_frequency"].format(
                limit=limit * 100, frequency=percentage * 100
            )
        )

    return {"value": sample_rate, "unit": "s"}  # type:ignore


def change_timezone(
    df: pd.DataFrame,
    source: ZoneInfo,
    target: ZoneInfo,
) -> pd.DataFrame:
    df = df.copy()
    df.index = df.index.tz_localize(source).tz_convert(target).tz_localize(None)  # type: ignore

    return df


def filter_by_datetime(
    df: pd.DataFrame,
    start: datetime | None = None,
    end: datetime | None = None,
) -> pd.DataFrame:
    if start and end:
        if end < start:
            raise ValueError(errors["invalid_datetime_interval"])

    if start:
        df = df[df.index >= start]

    if end:
        df = df[df.index <= end]

    if df.empty:
        raise ValueError(errors["empty_dataframe"])

    return df


def fix_columns(
    df: pd.DataFrame,
    extra_columns: bool = True,
) -> pd.DataFrame:
    # Order columns as defined in Column.
    records_columns = [col.value for col in Column]
    ordered_columns = [col for col in records_columns if col in df.columns]

    if extra_columns:
        # Append extra columns that are not in Column at the end, alphabetically
        extra = sorted(set(df.columns) - set(records_columns))
        ordered_columns.extend(extra)

    return df[ordered_columns]


def normalize_column_names(df: pd.DataFrame) -> None:
    """
    Normalizes the column names of the DataFrame.

    This function converts all column names in the DataFrame to lowercase and strips any leading or trailing whitespace.

    Args:
        df (pd.DataFrame): The DataFrame whose column names are to be normalized.

    Returns:
        None
    """

    df.columns = df.columns.str.lower().str.strip()


def get_unique_column_name(
    df: pd.DataFrame,
    length: int = 6,
) -> str:
    characters = string.ascii_letters + string.digits
    colname = "".join(secrets.choice(characters) for _ in range(length))

    while colname in df.columns.tolist():
        colname = "".join(secrets.choice(characters) for _ in range(length))

    return colname


def get_most_frequent_value(obj: list) -> Any:
    if isinstance(obj, list):
        ar = np.array(obj, dtype=str)
        vals, counts = np.unique(ar, return_counts=True)
        mode = vals[counts.argmax()]
        return mode.item()
