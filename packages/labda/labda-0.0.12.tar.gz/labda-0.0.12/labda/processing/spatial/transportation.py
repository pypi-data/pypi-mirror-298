from typing import Any

import pandas as pd
from pyproj import CRS

from ...preprocessing.expanders.spatial import get_speed
from ...preprocessing.utils.common import columns_checker
from ...structure.validation import Column


def _trip_mode_from_activity(df: pd.DataFrame) -> None:
    df.loc[
        (df["trip_mode"] == "vehicle")
        & (
            df["activity_intensity"].isin(
                ["moderate", "moderate-vigorous", "vigorous", "very vigorous"]
            )
        ),
        "trip_mode",
    ] = "bicycle"

    df.loc[
        (df["trip_mode"].isin(["bicycle", "walk/run"]))
        & (df["activity_intensity"] == "sedentary"),
        "trip_mode",
    ] = "vehicle"


def _fill_trip_mode_pauses(df: pd.DataFrame, fill: str) -> pd.DataFrame:
    if fill == "forward":
        df["trip_mode"] = df["trip_mode"].ffill()
    elif fill == "backward":
        df["trip_mode"] = df["trip_mode"].bfill()
    else:
        raise ValueError('Fill must be either "forward" or "backward".')

    return df


def _set_trip_mode(df: pd.DataFrame) -> None:
    modes = df["trip_mode"].mode()

    # FIXME: This is real problem, because mode is not always the best solution. Should be discussed. One idea is to ffill or bfill from other partial.
    dominant_mode = modes[0] if not modes.empty else None
    df["trip_mode"] = dominant_mode


# def _get_partial_trip_ids(df: pd.DataFrame) -> None:
#     df.loc[~df["trip_status"].isin(["stationary", "pause"]), "partials_id"] = (
#         df["trip_status"] == "start"
#     ).cumsum()


def _detect_partial_transport(
    df: pd.DataFrame,
    on: Column | str,
    cut_points: dict[str, Any],
    window: int | None = None,
    activity: bool = False,
) -> pd.Series:
    if window:
        df[on] = df[on].rolling(window=window, min_periods=1).mean()

    # Extract max values from cut_points.
    bins = [-float("inf")]
    bins += [cp["max"] for cp in cut_points["cut_points"]]

    # Extract names from cut_points.
    labels = [cp["name"] for cp in cut_points["cut_points"]]

    # Apply cut points
    df["trip_mode"] = pd.cut(df[on], bins=bins, labels=labels)

    if activity:
        # Fixes trip mode based on activity intensity.
        _trip_mode_from_activity(df)

    # Sets trip mode to the most common value in the partial.
    _set_trip_mode(df)

    return df["trip_mode"]


def detect_transportation(
    df: pd.DataFrame,
    crs: CRS,
    cut_points: dict[str, Any],
    window: int | None,
    pause_fill: str | None,
    activity: bool,
) -> pd.Series:
    required_column = cut_points["required_data"]
    cols = {
        Column.LATITUDE: "latitude",
        Column.LONGITUDE: "longitude",
        Column.TRIP_ID: "trip_id",
        Column.TRIP_STATUS: "trip_status",
        required_column: required_column,
    }

    if activity:
        cols[Column.ACTIVITY_INTENSITY] = "activity_intensity"

    cols_names = list(cols.values())
    columns_checker(df, cols_names, True)

    df = df[cols_names].copy()
    df.rename(columns=cols, inplace=True)

    if required_column == Column.SPEED:
        df["speed"] = get_speed(df, crs)

    # This was used with boundaries (start-end)
    # _get_partial_trip_ids(df)

    # df["trip_mode"] = (
    #     df.groupby(["trip_id", "partials_id"])
    #     .apply(
    #         lambda x: _detect_partial_transport(
    #             x, required_column, cut_points, window, activity
    #         ),
    #         include_groups=False,
    #     )
    #     .reset_index(level=[0, 1], drop=True)
    # )

    ids = (df["trip_status"] != (df["trip_status"].shift())).cumsum()
    df["trip_mode"] = (
        df[df["trip_status"] == "transport"]
        .groupby(ids)[cols_names]
        .apply(
            lambda x: _detect_partial_transport(
                x, required_column, cut_points, window, activity
            ),
            include_groups=False,
        )
    ).reset_index(level=0, drop=True)  # type: ignore

    if pause_fill:
        df["trip_mode"] = (
            df[["trip_id", "trip_mode"]]
            .groupby("trip_id")
            .apply(
                lambda x: _fill_trip_mode_pauses(x, pause_fill), include_groups=False
            )
            .reset_index(level=0, drop=True)
        )

    return df["trip_mode"].astype("category")
