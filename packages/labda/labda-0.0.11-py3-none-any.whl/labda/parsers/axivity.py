import logging
from pathlib import Path

import actipy
import pandas as pd

from ..logger import generate_subject_extra, object_parsed
from ..preprocessing.utils.common import (
    DEFAULT_TIMEZONE,
    check_file,
    check_size,
    extract_id,
    fix_columns,
    get_sampling_rate,
)
from ..structure import Metadata, SampleRate, Sensor, Subject
from ..structure.validation import Column, Placement, SampleRateUnit, Schema, Vendor

logger = logging.getLogger("labda")


def _rename_columns(df: pd.DataFrame) -> None:
    df.index.name = Column.DATETIME
    df.rename(
        columns={
            "x": Column.ACC_X,
            "y": Column.ACC_Y,
            "z": Column.ACC_Z,
        },
        inplace=True,
    )

    if "temperature" in df.columns:
        df.rename(
            columns={"temperature": Column.TEMPERATURE}, inplace=True
        )  # TODO: Check if it is in Celsius

    if "light" in df.columns:
        df.rename(
            columns={"light": Column.LUX}, inplace=True
        )  # TODO: Check if it is in Lux


def from_cwa(
    path: Path | str,
    lowpass: int | None = 20,
    calibrate: bool = True,
    resample: int | str = "uniform",
    *,
    subject_id: str | None = None,
    collection_id: str | None = None,
    sensor_id: str | None = None,
    serial_number: str | None = None,
    model: str | None = None,
    firmware_version: str | None = None,
    placement: Placement | None = None,
) -> Subject:
    path = check_file(path, "cwa")

    df, info = actipy.read_device(
        path.as_posix(),
        lowpass_hz=lowpass,  # type: ignore
        calibrate_gravity=calibrate,
        detect_nonwear=False,
        resample_hz=resample,  # type: ignore
        verbose=False,
    )

    if isinstance(resample, (int, float)):
        sample_rate = resample
    else:
        sample_rate = info.get("SampleRate")

    check_size(df)
    _rename_columns(df)
    df.sort_index(inplace=True)

    df = fix_columns(df, False)
    # df = Schema.validate(df)

    if not subject_id:
        subject_id = extract_id(path)

    if not sensor_id:
        sensor_id = info.get("DeviceID", subject_id)

    if sample_rate:
        sample_rate = SampleRate(value=sample_rate, unit=SampleRateUnit.HERTZ)
    else:
        sample_rate = get_sampling_rate(df)
        sample_rate = SampleRate.model_validate(sample_rate)

    vendor = Vendor.AXIVITY

    sensor = Sensor(
        id=sensor_id,  # type: ignore
        serial_number=serial_number,
        model=model,
        vendor=vendor,
        firmware_version=firmware_version,
        placement=placement,
    )

    metadata = Metadata(
        sensors=[sensor], sample_rate=sample_rate, crs=None, timezone=DEFAULT_TIMEZONE
    )

    subject = Subject(id=subject_id, collection=collection_id, metadata=metadata, df=df)

    object_parsed(subject, path.as_posix(), vendor, "from_cwa")

    if lowpass:
        logger.info(
            f"Lowpass filter: {lowpass:.1f}hz.",
            extra=generate_subject_extra(
                subject, "structure", "parsers", f"{vendor}.from_cwa"
            ),
        )

    if isinstance(resample, (int, float)):
        logger.info(
            f"Data resampled from {info.get('SampleRate'):.1f}hz to {metadata.sample_rate}.",
            extra=generate_subject_extra(
                subject, "structure", "parsers", f"{vendor}.from_cwa"
            ),
        )

    return subject
