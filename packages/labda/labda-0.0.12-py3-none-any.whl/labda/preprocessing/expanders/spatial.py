import warnings

import numpy as np
import pandas as pd
from pyproj import CRS

from ...structure.validation import Column
from ..utils.common import columns_checker, get_timedelta
from ..utils.spatial import df_to_gdf, get_crs_units


def get_distance(
    df: pd.DataFrame,
    crs: CRS,
) -> pd.Series:
    gdf = df_to_gdf(df, crs)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        distance = gdf.distance(gdf.shift(1))

    return distance


def get_speed(
    df: pd.DataFrame,
    crs: CRS,
) -> pd.Series:
    timedelta = get_timedelta(df)
    distance = get_distance(df, crs)

    speed = distance / timedelta.dt.total_seconds()

    # TODO: This is temporary fix for changing m/s to km/h for now.
    unit = get_crs_units(crs)

    if unit == "metre":
        speed = speed * 3.6
    else:
        raise ValueError(f"Unsupported unit: {unit}.")

    return speed


def get_acceleration(
    df: pd.DataFrame,
    crs: CRS,
) -> pd.Series:
    timedelta = get_timedelta(df)
    speed = get_speed(df, crs)

    acceleration = speed.diff(1) / timedelta.dt.total_seconds()

    return acceleration


def get_direction(
    df: pd.DataFrame,
) -> pd.Series:
    columns_checker(df, [Column.LATITUDE, Column.LONGITUDE], True)  # type: ignore

    # Convert to radians
    lon1, lat1 = np.radians(df[Column.LONGITUDE]), np.radians(df[Column.LATITUDE])
    lon2, lat2 = (
        np.radians(df[Column.LONGITUDE].shift()),
        np.radians(df[Column.LATITUDE].shift()),
    )

    dlon = lon2 - lon1

    x = np.cos(lat2) * np.sin(dlon)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)

    direction = np.arctan2(x, y)
    direction = np.degrees(direction)
    direction = (direction + 360) % 360
    direction = pd.Series(direction, index=df.index)

    return direction


def get_elevation(df: pd.DataFrame) -> pd.Series:
    raise NotImplementedError("This function is not implemented yet.")


def get_weather(df: pd.DataFrame) -> pd.Series:
    raise NotImplementedError("This function is not implemented yet.")


def get_address(df: pd.DataFrame) -> pd.Series:
    raise NotImplementedError("This function is not implemented yet.")
