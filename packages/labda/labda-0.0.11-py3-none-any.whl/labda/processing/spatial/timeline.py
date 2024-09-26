import pandas as pd
from pyproj import CRS
from shapely.geometry import LineString

from ...preprocessing.expanders.spatial import get_distance
from ...preprocessing.utils.common import columns_checker
from ...preprocessing.utils.spatial import df_to_gdf
from ...structure.validation import Column


def _get_summary(df: pd.DataFrame, crs: CRS, type: str) -> pd.Series:
    start = df.index.min()
    end = df.index.max()
    duration = end - start

    summary = {
        "segment_id": df[Column.SEGMENT_ID].iloc[0],
        "start": df.index.min(),
        "end": df.index.max(),
        "duration": duration,
        "trip_status": type,
    }
    geometry = df_to_gdf(df, crs).geometry

    if type == "trip":
        summary["trip_id"] = df[Column.TRIP_ID].iloc[0]

        if "trip_mode" in df.columns:
            summary["trip_mode"] = df[Column.TRIP_MODE].iloc[0]

        summary["distance"] = get_distance(df, crs).sum()
        summary["geometry"] = LineString(geometry)
    else:
        summary["stationary_id"] = df[Column.STATIONARY_ID].iloc[0]
        summary["geometry"] = geometry.union_all()

        if type == "pause":
            summary["trip_id"] = df[Column.TRIP_ID].iloc[0]

    return pd.Series(summary)


def get_timeline(df: pd.DataFrame, crs: CRS) -> pd.DataFrame:
    cols = [
        Column.LATITUDE,
        Column.LONGITUDE,
        Column.SEGMENT_ID,
        Column.TRIP_ID,
        Column.STATIONARY_ID,
        Column.TRIP_STATUS,
        Column.TRIP_MODE,
    ]
    columns_checker(df, cols, True)  # type: ignore

    ids = (df["trip_status"] != (df["trip_status"].shift())).cumsum()

    trips = (
        df[df["trip_status"] == "transport"]
        .groupby(ids)[cols]
        .apply(lambda x: _get_summary(x, crs, "trip"))
    )  # type: ignore
    stationary = (
        df[df["trip_status"] == "stationary"]
        .groupby(ids)[cols]
        .apply(lambda x: _get_summary(x, crs, "stationary"))
    )  # type: ignore
    pauses = (
        df[df["trip_status"] == "pause"]
        .groupby(ids)[cols]
        .apply(lambda x: _get_summary(x, crs, "pause"))
    )  # type: ignore

    dfs = []
    for df in [trips, stationary, pauses]:
        if not df.empty:
            dfs.append(df)

    timeline = pd.concat(dfs).sort_values("start")  # type: ignore
    timeline.index.name = "id"

    return timeline[
        [
            "start",
            "end",
            "duration",
            "trip_status",
            "segment_id",
            "trip_id",
            "stationary_id",
            "trip_mode",
            "distance",
            "geometry",
        ]
    ]
