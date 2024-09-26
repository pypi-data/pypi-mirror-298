from typing import Any

from ...structure.validation import Column
from .utils import mode, sum

UNIFORM: dict[Column, Any] = {
    # --- Base ---
    Column.SUBJECT_ID: "first",
    Column.TIMEDELTA: sum,
    Column.WEAR: mode,
    # --- Counts ---
    Column.COUNTS_X: sum,
    Column.COUNTS_Y: sum,
    Column.COUNTS_Z: sum,
    Column.COUNTS_VM: "mean",
    # --- Taxonomy ---
    Column.MOVEMENT: mode,
    Column.ACTION: mode,
    Column.ACTIVITY: mode,
    # --- Other ---
    Column.ACTIVITY_INTENSITY: mode,
    Column.ACTIVITY_VALUE: "mean",
    Column.STEPS: sum,
    Column.HEART_RATE: "mean",
    Column.TEMPERATURE: "mean",
    Column.LUX: "mean",
    # --- Spatial ---
    Column.LATITUDE: "first",
    Column.LONGITUDE: "first",
    Column.GNSS_ACCURACY: "first",
    Column.NSAT_VIEWED: "first",
    Column.NSAT_USED: "first",
    Column.NSAT_RATIO: "first",
    Column.SNR_VIEWED: "first",
    Column.SNR_USED: "first",
    Column.PDOP: "first",
    Column.HDOP: "first",
    Column.VDOP: "first",
    Column.DISTANCE: sum,
    Column.ELEVATION: "first",
    Column.SPEED: "mean",
    Column.ACCELERATION: "mean",
    Column.DIRECTION: "first",
    Column.ENVIRONMENT: mode,
}
