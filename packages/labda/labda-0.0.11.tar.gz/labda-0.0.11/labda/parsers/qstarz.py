import logging
from pathlib import Path

import numpy as np
import pandas as pd

from ..logger import generate_extra, object_parsed
from ..logs import errors
from ..preprocessing.utils.common import (
    DEFAULT_TIMEZONE,
    check_file,
    check_size,
    columns_exists,
    extract_id,
    fix_columns,
    get_sampling_rate,
    normalize_column_names,
)
from ..preprocessing.utils.spatial import DEFAULT_CRS
from ..structure import Metadata, SampleRate, Sensor, Subject
from ..structure.validation import Column, Placement, Schema, Vendor

logger = logging.getLogger("labda")


def _remove_invalid_rows(df: pd.DataFrame) -> None:
    if "valid" in df.columns:
        df["valid"] = df["valid"].str.lower()
        indexes = df[
            (df["valid"].isin(["no fix", "estimated (dead reckoning)", "unknown mode"]))
        ].index
        df.drop(indexes, inplace=True)


def _remove_repeated_headers(df: pd.DataFrame) -> None:
    """
    Removes the rows from the DataFrame that are identical to the header.

    This function identifies the rows that are identical to the header in the DataFrame and removes them in-place.

    Args:
        df (pd.DataFrame): The DataFrame from which to remove the rows identical to the header.

    Returns:
        None
    """

    header = df.columns
    indexes = df[df.eq(header).all(axis=1)].index
    df.drop(indexes, inplace=True)


def _drop_specific_columns(df: pd.DataFrame, columns: list[str]) -> None:
    """
    Drops specific columns from a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame from which to drop columns.
        columns (list[str]): A list of column names to be dropped.

    Returns:
        None
    """

    for column in columns:
        if column in df.columns:
            df.drop(columns=column, inplace=True)


def _parse_coordinates(df: pd.DataFrame) -> None:
    """
    Parses and normalizes the latitude and longitude coordinates in the DataFrame.

    This function checks for the existence of the required columns ("latitude", "longitude", "n/s", "e/w"),
    renames them to standardized column names, converts the latitude and longitude values to numeric,
    and adjusts the sign based on the "n/s" and "e/w" indicators. It then drops the "n/s" and "e/w" columns.

    Args:
        df (pd.DataFrame): The DataFrame containing the coordinate columns to be parsed.

    Raises:
        ValueError: If any of the required columns ("latitude", "longitude", "n/s", "e/w") do not exist in the DataFrame.

    Returns:
        None
    """

    columns_exists(df, ["latitude", "longitude", "n/s", "e/w"])
    df.rename(
        columns={"latitude": Column.LATITUDE, "longitude": Column.LONGITUDE},
        inplace=True,
    )
    df[[Column.LATITUDE, Column.LONGITUDE]] = df[
        [Column.LATITUDE, Column.LONGITUDE]
    ].apply(pd.to_numeric)

    df[Column.LATITUDE] = np.where(
        df["n/s"] == "S", -df[Column.LATITUDE], df[Column.LATITUDE]
    )
    df[Column.LONGITUDE] = np.where(
        df["e/w"] == "W", -df[Column.LONGITUDE], df[Column.LONGITUDE]
    )

    df.drop(columns=["n/s", "e/w"], inplace=True)


def _parse_datetime(
    df: pd.DataFrame,
    format: str | None = None,
    drop_duplicates: bool = True,
) -> None:
    """
    Parses and normalizes the datetime information in the DataFrame.

    This function checks for the existence of date and time columns, combines them into a single datetime column,
    and converts it to a datetime object. If only a single datetime column is present, it renames it to a standardized
    column name. It also drops rows with invalid datetime values.

    Args:
        df (pd.DataFrame): The DataFrame containing the datetime columns to be parsed.
        dt_format (str, optional): The format of the datetime strings. Defaults to None.
        drop_duplicates (bool, optional): Whether to drop duplicate rows based on the datetime column. Defaults to True.

    Raises:
        ValueError: If the required date and time columns do not exist in the DataFrame.

    Returns:
        None
    """

    date, time, column = None, None, None

    if "date" in df.columns and "time" in df.columns:
        date, time = "date", "time"
    elif "utc date" in df.columns and "utc time" in df.columns:
        date, time = "utc date", "utc time"
    elif "utc" in df.columns:
        column = "utc"
    else:
        raise ValueError(errors["missing_datetime_columns"])

    if column:
        df.rename(columns={column: Column.DATETIME}, inplace=True)
    elif date and time:
        df[[date, time]] = df[[date, time]].astype("string")
        df[Column.DATETIME] = df[date] + " " + df[time]
        df.drop(columns=[date, time], inplace=True)

    df[Column.DATETIME] = pd.to_datetime(
        df[Column.DATETIME], format=format, errors="coerce"
    )

    df.dropna(subset=[Column.DATETIME], inplace=True)

    if drop_duplicates:
        df.drop_duplicates(subset=[Column.DATETIME], inplace=True)

    df.set_index(Column.DATETIME, inplace=True, drop=True)
    df.sort_index(inplace=True)


def _parse_distance(
    df: pd.DataFrame,
    columns: list[str],
) -> None:
    """
    Parse the distance column(s) in the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the distance column(s).
        columns (list[str]): The list of column names to parse.

    Returns:
        None
    """

    for column in columns:
        if column in df.columns:
            if df[column].dtype == "object":
                df[column] = df[column].str.strip("M")
            df[column] = pd.to_numeric(df[column])
            df[column] = df[column].round(2)
            df.rename(columns={column: Column.DISTANCE}, inplace=True)

            break

    if column in df.columns:
        df[column] = pd.to_numeric(df[column])
        df[column] = df[column].round(2)
        df.rename(columns={column: Column.DISTANCE}, inplace=True)


def _parse_speed(df: pd.DataFrame, columns: list[str]) -> None:
    """
    Parse the speed column(s) in the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the speed column(s).
        columns (list[str]): The list of column names to parse.

    Returns:
        None
    """

    for column in columns:
        if column in df.columns:
            if df[column].dtype == "object":
                df[column] = df[column].str.strip("km/h")
            df[column] = pd.to_numeric(df[column])
            df[column] = (df[column] / 3.6).round(2)
            df.rename(columns={column: Column.SPEED}, inplace=True)

            break


def _parse_elevation(df: pd.DataFrame, columns: list[str]) -> None:
    """
    Parses elevation data in the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the elevation data.
        columns (list[str]): A list of column names to search for elevation data.

    Returns:
        None
    """

    for column in columns:
        if column in df.columns:
            if df[column].dtype == "object":
                df[column] = df[column].str.strip("M")
            df[column] = pd.to_numeric(df[column])
            df[column] = df[column].round(2)
            df.rename(columns={column: Column.ELEVATION}, inplace=True)

            break


def _parse_dop(df: pd.DataFrame) -> None:
    """
    Parses the dilution of precision (DOP) values from a DataFrame.
    This function renames the columns in the DataFrame to standard DOP column names.

    Args:
        df (pd.DataFrame): The DataFrame containing the DOP values.

    Returns:
        None
    """

    column_mapping = {
        "hdop": Column.HDOP,
        "vdop": Column.VDOP,
        "pdop": Column.PDOP,
    }

    for old_column, new_column in column_mapping.items():
        if old_column in df.columns:
            df.rename(columns={old_column: new_column}, inplace=True)


def _parse_nsat(df: pd.DataFrame, path: Path, vendor: Vendor) -> None:
    """
    Parses the 'nsat' column in the given DataFrame and updates it accordingly.

    Args:
        df (pd.DataFrame): The DataFrame containing the 'nsat' column.

    Returns:
        None
    """

    column = "nsat"

    if column in df.columns:
        df[column] = df[column].astype("string")
        df.rename(columns={column: Column.NSAT_USED}, inplace=True)
        df[Column.NSAT_USED] = pd.to_numeric(df[Column.NSAT_USED])
    else:
        column = next(
            (column for column in df.columns if "nsat" in column), None
        )  # "NSAT (USED/VIEW)", "NSAT(USED/VIEW)", "NSAT(USED/VIEWED)"
        try:
            if column:
                df[column] = df[column].astype("string")

                if df[column].str.contains("/").any():
                    df[column] = df[column].str.split("/")
                elif df[column].str.contains(r"\(").any():  # Maybe this is wrong
                    df[column] = df[column].str.replace(")", "").str.split("(")

                df[Column.NSAT_USED] = pd.to_numeric(df[column].str[0])
                df[Column.NSAT_VIEWED] = pd.to_numeric(df[column].str[1])
                df.drop(columns=[column], inplace=True)
        except Exception:
            logger.warning(
                f"Could not parse 'nsat' column from file {path.as_posix()}.",
                extra=generate_extra(
                    None,
                    "other",
                    "structure",
                    "parsers",
                    f"{vendor.lower()}.from_csv",
                ),
            )


def _get_used_snr(signal):
    snr_type = signal.split("-")

    if "#" in snr_type[0]:
        return int(snr_type[-1])
    else:
        return 0


def _parse_snr(df: pd.DataFrame, columns: list[str]) -> None:
    """
    Parses the SNR (Signal-to-Noise Ratio) values in the specified columns of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        columns (list[str]): The list of column names to parse.

    Returns:
        None
    """

    for column in columns:
        if column in df.columns:
            df[column] = df[column].astype("string")
            df.loc[df[column].str.contains("/"), column] = pd.NA

            temp_df = df[[column]]
            temp_df = temp_df[temp_df[column].notna()]
            temp_df[column] = temp_df[column].str.split(";")

            if (
                Column.NSAT_VIEWED not in df.columns
                and Column.NSAT_USED not in df.columns
            ):
                df[Column.NSAT_VIEWED] = temp_df[column].apply(lambda row: len(row))

            temp_df[Column.SNR_USED] = temp_df[column].apply(
                lambda row: sum([_get_used_snr(signal) for signal in row])
            )
            temp_df[Column.SNR_VIEWED] = temp_df[column].apply(
                lambda row: sum([int(signal.split("-")[-1]) for signal in row])
            )

            df[[Column.SNR_USED, Column.SNR_VIEWED]] = temp_df[
                [Column.SNR_USED, Column.SNR_VIEWED]
            ]

            df.drop(columns=[column], inplace=True)

            break


def _calculate_snr_ratio(df: pd.DataFrame) -> None:
    if Column.NSAT_USED in df.columns and Column.NSAT_VIEWED in df.columns:
        df[Column.NSAT_RATIO] = (
            (df[Column.NSAT_USED] * 100) / df[Column.NSAT_VIEWED]
        ).round(2)


def _detect_environment(
    df: pd.DataFrame,
    method: Column,
    limit: int | float,
):
    methods = [
        Column.SNR_USED,  # 225 (F1: 46,80)
        Column.SNR_VIEWED,  # 260 (F1: 71,18)
        Column.NSAT_USED,  # 7 (F1: 48,86)
        Column.NSAT_VIEWED,  # 9 (F1: 42,93)
        Column.NSAT_RATIO,  # 70 (F1: 46,40)
    ]
    if method not in methods:
        raise ValueError(
            errors["invalid_method"].format(method=method, valid_methods=methods)
        )

    if method not in df.columns:
        raise ValueError(f"Column '{method}' does not exist in dataframe")

    mask = df[method].notna()
    df.loc[mask, Column.ENVIRONMENT] = "outdoor"
    df.loc[mask & (df[method] <= limit), Column.ENVIRONMENT] = "indoor"


def from_csv(
    path: Path | str,
    *,
    subject_id: str | None = None,
    collection_id: str | None = None,
    sensor_id: str | None = None,
    serial_number: str | None = None,
    model: str | None = None,
    firmware_version: str | None = None,
    placement: Placement | None = None,
    datetime_format: str | None = None,
    environment_method: Column | None = None,
    environment_limit: float | None = None,
) -> Subject:
    crs = DEFAULT_CRS
    timezone = DEFAULT_TIMEZONE
    vendor = Vendor.QSTARZ

    path = check_file(path, "csv")
    df = pd.read_csv(path, engine="pyarrow")

    _drop_specific_columns(df, [""])
    _remove_repeated_headers(df)
    normalize_column_names(df)
    _remove_invalid_rows(df)
    check_size(df)
    _parse_coordinates(df)
    _parse_datetime(df, datetime_format)
    _parse_distance(df, ["distance(m)", "distance"])
    _parse_speed(df, ["speed", "speed(km/h)", "speed_kmh"])
    _parse_elevation(df, ["height", "height(m)", "height_m"])
    _parse_dop(df)
    _parse_nsat(df, path, vendor)
    _parse_snr(
        df, ["sat info (sid-ele-azi-snr)", "sat info (sid-snr)", "snr", "satinfo"]
    )

    _calculate_snr_ratio(df)

    if environment_method and environment_limit:
        _detect_environment(df, environment_method, environment_limit)
    else:
        if Column.SNR_VIEWED in df.columns:
            _detect_environment(df, Column.SNR_VIEWED, 260)
        elif Column.NSAT_RATIO in df.columns:
            _detect_environment(df, Column.NSAT_RATIO, 70)

    df = fix_columns(df, False)
    df = Schema.validate(df)

    if not subject_id:
        subject_id = extract_id(path)

    if not sensor_id:
        sensor_id = subject_id

    sample_rate = get_sampling_rate(df)
    sample_rate = SampleRate.model_validate(sample_rate)

    sensor = Sensor(
        id=sensor_id,
        serial_number=serial_number,
        model=model,
        vendor=vendor,
        firmware_version=firmware_version,
        placement=placement,
    )

    metadata = Metadata(
        sensors=[sensor],
        sample_rate=sample_rate,
        crs=crs,
        timezone=timezone,
    )

    subject = Subject(
        id=subject_id,
        collection=collection_id,
        metadata=metadata,
        df=df,
    )

    object_parsed(subject, path.as_posix(), vendor, "from_csv")

    return subject
