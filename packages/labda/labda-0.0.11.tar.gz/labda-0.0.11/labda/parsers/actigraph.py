from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
from dateutil.parser import parse as parse_dt

from ..logger import object_parsed
from ..preprocessing.utils.common import (
    check_file,
    check_size,
    extract_id,
    fix_columns,
    get_sampling_rate,
    normalize_column_names,
)
from ..structure import Metadata, SampleRate, Sensor, Subject
from ..structure.validation import Column, Placement, SampleRateUnit, Schema, Vendor


def _parse_metadata(
    header: list[str],
    datetime_format: str | None,
) -> dict[str, Any]:
    model = header[0].split("ActiGraph")[-1].split()[0].strip()
    firmware = header[0].split("Firmware")[-1].split()[0].strip()
    serial_number = header[1].split()[-1].strip()
    start_time = header[2].split()[-1].strip()
    start_date = header[3].split()[-1].strip()
    dt = start_date + " " + start_time
    if datetime_format:
        start_datetime = datetime.strptime(dt, datetime_format)
    else:
        start_datetime = parse_dt(start_date + " " + start_time)
    sampling_frequency = pd.to_timedelta(header[4].split()[-1].strip()).total_seconds()

    return {
        "model": model,
        "firmware": firmware,
        "serial_number": serial_number,
        "start_datetime": start_datetime,
        "sample_rate": sampling_frequency,
    }


def _parse_df_with_header(data: list[str]) -> pd.DataFrame:
    df_header = data[0].split(",")
    df = data[1:]
    df = pd.DataFrame(df)
    df = df[0].str.split(",", expand=True)
    df.columns = df_header
    normalize_column_names(df)

    column_mapping = {
        "epoch": "time",
        "axis1": Column.COUNTS_X,
        "axis2": Column.COUNTS_Y,
        "axis3": Column.COUNTS_Z,
        "activity": Column.COUNTS_X,
        "activity (horizontal)": Column.COUNTS_Y,
        "3rd axis": Column.COUNTS_Z,
        "vector magnitude": Column.COUNTS_VM,
        "vm": Column.COUNTS_VM,
        "steps": Column.STEPS,
        "lux": Column.LUX,
        "inclinometer off": "non-wear",
        "inclinometer standing": "standing",
        "inclinometer sitting": "sitting",
        "inclinometer lying": "lying",
    }

    for old_column, new_column in column_mapping.items():
        if old_column in df.columns:
            df.rename(columns={old_column: new_column}, inplace=True)

    if Column.COUNTS_VM in df.columns and df[Column.COUNTS_VM].dtype == object:
        df[Column.COUNTS_VM] = df[Column.COUNTS_VM].str.replace('"', "")

    return df


def _parse_inclinometer(df: pd.DataFrame) -> pd.DataFrame:
    columns = ["non-wear", "standing", "sitting", "lying"]
    exists_columns = []

    for column in columns:
        if column in df.columns:
            exists_columns.append(column)

    if exists_columns:
        df["inclinometer"] = df[exists_columns].idxmax(axis=1)

    if "non-wear" in exists_columns:
        df[Column.WEAR] = True
        df.loc[df["inclinometer"] == "non-wear", Column.WEAR] = False
        df.loc[~df[Column.WEAR], "inclinometer"] = pd.NA

    df.drop(columns=exists_columns, inplace=True)

    return df


def _parse_df_without_header(data: list[str]) -> pd.DataFrame:
    df = pd.DataFrame(
        data,
    )
    df = df[0].str.split(",", expand=True)
    df = df.iloc[:, :3]
    df.columns = [
        Column.COUNTS_X,
        Column.COUNTS_Y,
        Column.COUNTS_Z,
    ]

    return df


def _load_data(
    path: Path,
    line: int,
    header: bool,
    datetime_format: str | None,
) -> tuple[pd.DataFrame, dict[str, Any] | None]:
    metadata = None

    with path.open("r") as f:
        file = f.read()

    lines = file.splitlines()
    data = lines[line:]

    if header:
        metadata = _parse_metadata(lines[0:line], datetime_format)

    if any(char.isalpha() for char in data[0]):
        df = _parse_df_with_header(data)
        _parse_inclinometer(
            df
        )  # This is only for detecting the non-wear, later on the inclinometer column is dropped.
    else:
        df = _parse_df_without_header(data)

    return df, metadata


def _parse_datetime(
    df: pd.DataFrame,
    metadata: dict[str, Any] | None,
    dt_format: str | None = None,
) -> None:
    if "date" in df.columns and "time" in df.columns:
        df[Column.DATETIME] = pd.to_datetime(
            df["date"] + " " + df["time"], format=dt_format
        )
        df.drop(columns=["date", "time"], inplace=True)

    elif metadata:
        start_datetime = metadata["start_datetime"]
        sample_rate = metadata["sample_rate"]
        df[Column.DATETIME] = pd.date_range(
            start_datetime, periods=len(df), freq=timedelta(seconds=sample_rate)
        )

    df.dropna(subset=[Column.DATETIME], inplace=True)
    df.set_index(Column.DATETIME, inplace=True)
    df.sort_index(inplace=True)


def from_csv(
    path: Path | str,
    line: int = 10,
    header: bool = True,
    *,
    subject_id: str | None = None,
    collection_id: str | None = None,
    sensor_id: str | None = None,
    serial_number: str | None = None,
    model: str | None = None,
    firmware_version: str | None = None,
    placement: Placement | None = None,
    datetime_format: str | None = None,
    timezone: ZoneInfo | None = None,
) -> Subject:
    # Tested only for CSV with counts in seconds, not for Hz!
    path = check_file(path, "csv")

    df, metadata = _load_data(path, line, header, datetime_format)
    check_size(df)

    _parse_datetime(df, metadata, datetime_format)

    df = fix_columns(df, False)
    df = Schema.validate(df)

    if not subject_id:
        subject_id = extract_id(path)

    if not sensor_id:
        sensor_id = subject_id

    if not metadata:
        sample_rate = get_sampling_rate(df)
        sample_rate = SampleRate.model_validate(sample_rate)
    else:
        sample_rate = SampleRate(
            value=metadata["sample_rate"], unit=SampleRateUnit.SECOND
        )

    vendor = Vendor.ACTIGRAPH

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
        crs=None,
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
