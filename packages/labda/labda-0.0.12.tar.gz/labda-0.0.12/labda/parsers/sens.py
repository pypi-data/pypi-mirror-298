from pathlib import Path

import numpy as np
import pandas as pd

from ..logger import object_parsed
from ..preprocessing.utils.common import (
    DEFAULT_TIMEZONE,
    check_file,
    check_size,
    extract_id,
    fix_columns,
    get_sampling_rate,
    normalize_column_names,
)
from ..structure import Metadata, SampleRate, Sensor, Subject
from ..structure.validation import Column, Placement, SampleRateUnit, Schema, Vendor


def _parse_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        engine="pyarrow",
    )

    normalize_column_names(df)

    boolean_cols = [
        "general/nodata/time",
        "activity/lying_sitting_rest/time",
        "activity/lying_sitting_movement/time",
        "activity/upright_stand/time",
        "activity/upright_sporadic_walk/time",
        "activity/upright_walk/time",
        "activity/upright_moderate/time",
        "activity/upright_run/time",
        "activity/cycling/time",
        "activity/sit2stand/count",
    ]
    df[boolean_cols] = df[boolean_cols].astype("boolean")

    if "unixts" not in df.columns:
        raise ValueError("No datetime column found.")

    df["unixts"] = pd.to_datetime(df["unixts"], unit="ms")
    df.rename(columns={"unixts": Column.DATETIME}, inplace=True)
    df.set_index(Column.DATETIME, inplace=True)
    df.sort_index(inplace=True)

    return df


def _check_sample_rate(df: pd.DataFrame) -> SampleRate:
    sample_rate = get_sampling_rate(df)
    sample_rate["value"] = round(sample_rate["value"])

    if sample_rate["value"] != 5:
        raise ValueError(
            "Invalid sampling rate. Are you sure this is a 5s epoch CSV file from Sens?"
        )

    sample_rate = SampleRate.model_validate(sample_rate)

    return sample_rate


def _infer_steps(df: pd.DataFrame) -> None:
    # 'activity/steps/count'
    # 'activity/steps2/count'
    # 'activity/steps3/count'
    df[Column.STEPS] = (
        df["activity/steps/count"]
        + df["activity/steps2/count"]
        + df["activity/steps3/count"]
    )

    df.drop(
        columns=[
            "activity/steps/count",
            "activity/steps2/count",
            "activity/steps3/count",
        ],
        inplace=True,
    )


def _infer_activity_intensity(df: pd.DataFrame) -> None:
    df.rename(columns={"activity/intensity/count": Column.ACTIVITY_VALUE}, inplace=True)
    # 'activity/intensity/count'
    labels = ["sedentary", "light", "moderate", "vigorous", "very vigorous"]
    cuts = [0, 2, 50, 75, 100, float("inf")]

    df[Column.ACTIVITY_INTENSITY] = pd.cut(
        df[Column.ACTIVITY_VALUE],
        bins=cuts,
        labels=labels,
        right=False,
        include_lowest=True,
    )


def _infer_non_wear(df: pd.DataFrame) -> None:
    # 'general/nodata/time': Non-wear
    df["general/nodata/time"] = ~df["general/nodata/time"]
    df.rename(columns={"general/nodata/time": Column.WEAR}, inplace=True)


def _infer_actions(df: pd.DataFrame) -> None:
    # 'activity/lying_sitting_rest/time': Sedentary behavior
    df.loc[df["activity/lying_sitting_rest/time"], Column.ACTION] = "lying-sitting"

    # 'activity/upright_stand/time': Standing
    df.loc[df["activity/upright_stand/time"], Column.ACTION] = "standing"

    # 'activity/cycling/time': Based on the pattern of the data, this is cycling.
    df.loc[df["activity/cycling/time"], Column.ACTION] = "cycling"

    # 'activity/upright_walk/time': Based on the pattern of the data, this is walking.
    df.loc[df["activity/upright_walk/time"], Column.ACTION] = "walking"

    # 'activity/sit2stand/count': Standing up
    df.loc[df["activity/sit2stand/count"], Column.ACTION] = "standing up"

    # 'activity/upright_sporadic_walk/time': Slow cycling, sporadic walking or other movements while standing.
    # 'activity/upright_moderate/time': Jogging or moderate intensity training, not based on pattern of the data.
    # 'activity/upright_run/time': Run or high intensity training, not based on pattern of the data.
    # 'activity/lying_sitting_movement/time': Slow cycling or other movements while sitting.

    df.drop(
        columns=[
            "activity/lying_sitting_rest/time",
            "activity/lying_sitting_movement/time",
            "activity/upright_stand/time",
            "activity/upright_sporadic_walk/time",
            "activity/upright_walk/time",
            "activity/upright_moderate/time",
            "activity/upright_run/time",
            "activity/cycling/time",
            "activity/sit2stand/count",
        ],
        inplace=True,
    )


def from_activities(
    path: Path | str,
    *,
    subject_id: str | None = None,
    collection_id: str | None = None,
    sensor_id: str | None = None,
    serial_number: str | None = None,
    model: str | None = None,
    firmware_version: str | None = "v5.4",
    placement: Placement | None = Placement.THIGH,
) -> Subject:
    path = check_file(path, "csv")

    if firmware_version != "v5.4":
        raise ValueError("Only Sens firmware version 5.4 is supported.")

    df = _parse_csv(path)
    check_size(df)

    sample_rate = _check_sample_rate(df)

    _infer_non_wear(df)
    _infer_actions(df)
    _infer_activity_intensity(df)
    _infer_steps(df)

    df = fix_columns(df, False)
    df = Schema.validate(df)

    if not subject_id:
        subject_id = extract_id(path)

    if not sensor_id:
        sensor_id = subject_id

    vendor = Vendor.SENS

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
        timezone=DEFAULT_TIMEZONE,
    )

    subject = Subject(
        id=subject_id,
        collection=collection_id,
        metadata=metadata,
        df=df,
    )

    object_parsed(subject, path.as_posix(), vendor, "from_activities")

    return subject


def _parse_binary(path: Path) -> pd.DataFrame:
    bytes_per_sample = 12

    samples = path.stat().st_size // bytes_per_sample

    dt = np.dtype(
        [
            (Column.DATETIME, "6uint8"),
            (Column.ACC_X, ">i2"),
            (Column.ACC_Y, ">i2"),
            (Column.ACC_Z, ">i2"),
        ]
    )
    data = np.fromfile(path, dtype=dt, count=samples)

    timestamps = data[Column.DATETIME].view("uint8").reshape(samples, 6)
    timestamps = np.dot(
        timestamps, [1 << 40, 1 << 32, 1 << 24, 1 << 16, 1 << 8, 1]
    ).astype(np.uint64)

    array = np.column_stack(
        (timestamps, data[Column.ACC_X], data[Column.ACC_X], data[Column.ACC_X])
    )
    df = pd.DataFrame(
        array, columns=[Column.DATETIME, Column.ACC_X, Column.ACC_Y, Column.ACC_Z]
    )

    df[Column.DATETIME] = pd.to_datetime(df[Column.DATETIME], unit="ms")
    df.set_index(Column.DATETIME, inplace=True)
    df.sort_index(inplace=True)

    return df


def _parse_raw_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        engine="pyarrow",
    )

    normalize_column_names(df)

    if "unixts" not in df.columns:
        raise ValueError("No datetime column found.")

    df["unixts"] = pd.to_datetime(df["unixts"], unit="ms")
    df.rename(
        columns={
            "unixts": Column.DATETIME,
            "x": Column.ACC_X,
            "y": Column.ACC_Y,
            "z": Column.ACC_Z,
        },
        inplace=True,
    )
    df.set_index(Column.DATETIME, inplace=True)
    df.sort_index(inplace=True)

    return df[[Column.ACC_X, Column.ACC_Y, Column.ACC_Z]]


def from_raw(
    path: Path | str,
    *,
    subject_id: str | None = None,
    collection_id: str | None = None,
    sensor_id: str | None = None,
    serial_number: str | None = None,
    model: str | None = None,
    firmware_version: str | None = None,
    placement: Placement | None = Placement.THIGH,
) -> Subject:
    if isinstance(path, str):
        path = Path(path)

    if path.suffix == ".bin":
        path = check_file(path, "bin")
        df = _parse_binary(path)
    elif path.suffix == ".csv":
        path = check_file(path, "csv")
        df = _parse_raw_csv(path)
    else:
        raise ValueError("Only binary and CSV files are supported.")

    check_size(df)

    df = fix_columns(df, False)
    df = Schema.validate(df)

    sample_rate = get_sampling_rate(df)
    sample_rate = SampleRate.model_validate(sample_rate)
    sample_rate.set_unit(SampleRateUnit.HERTZ)

    if not subject_id:
        subject_id = extract_id(path)

    if not sensor_id:
        sensor_id = subject_id

    vendor = Vendor.SENS

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
        timezone=DEFAULT_TIMEZONE,
    )

    subject = Subject(
        id=subject_id,
        collection=collection_id,
        metadata=metadata,
        df=df,
    )

    object_parsed(subject, path.as_posix(), vendor, "from_raw")

    return subject
