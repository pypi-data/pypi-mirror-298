from datetime import timedelta

import numpy as np
import pandas as pd
from pyproj import CRS

from ...logs import errors
from ...preprocessing.expanders.spatial import get_distance
from ...preprocessing.filtering.spatial import min_distance_filter
from ...preprocessing.splitting.common import gap_splitter
from ...preprocessing.splitting.spatial import stop_splitter
from ...structure.validation import Column

TRIP_STATUS = [
    "start",
    "end",
    "transport",
    "pause",
    "stationary",
]


def _convert_distance_parameter(
    param: int | float, sampling_frequency: timedelta
) -> float:
    meters = param / (60 / sampling_frequency.total_seconds())
    return meters


def _add_boundaries(
    df: pd.DataFrame,
    id_col: str,
    status_col: str,
) -> None:
    # If 'transport' is at the start or end of the DataFrame, change it to 'start' or 'end' respectively.
    if df.iloc[0][status_col] == "transport":
        df.iloc[0, df.columns.get_loc(status_col)] = "start"  # type: ignore
    if df.iloc[-1][status_col] == "transport":
        df.iloc[-1, df.columns.get_loc(status_col)] = "end"  # type: ignore

    # Create a temporary DataFrame that shifts the trip status by 1 row forward and backward.
    temp_df_prev = df.shift(1)
    temp_df_next = df.shift(-1)

    # Change the points immediately after a "transport" sequence to "end".
    df.loc[
        (
            (temp_df_prev[status_col] == "start")
            | (temp_df_prev[status_col] == "transport")
        )
        & ((df[status_col] == "stationary") | (df[status_col] == "pause")),
        status_col,
    ] = "end"

    # Change the points immediately before a "transport" sequence to "start"
    df.loc[
        (temp_df_next[status_col] == "transport")
        & ((df[status_col] == "stationary") | (df[status_col] == "pause")),
        status_col,
    ] = "start"

    df["group"] = (df[status_col] == "start").cumsum().astype("UInt16")
    df.loc[df[status_col] == "stationary", "group"] = pd.NA
    df[id_col] = df.groupby("group")[id_col].transform("first")
    df.drop(columns=["group"], inplace=True)


def _adjust_stationary_statutes(df: pd.DataFrame) -> None:
    # Create a new column 'group' that increments by 1 whenever the 'trip_status' changes
    df["group"] = (df["trip_status"] != df["trip_status"].shift()).cumsum()

    if df["group"].nunique() == 1:
        return

    # Get the minimum group ID.
    min_id = df["group"].min()

    # Get the maximum group ID.
    max_id = df["group"].max()

    first_value = df["group"].iloc[0]
    last_value = df["group"].iloc[-1]

    # If the first or last group is 'pause', change the group to 'stationary', so the trip starts and ends with 'stationary'.
    if first_value == "pause" or first_value == "start":
        df.loc[df["group"] == min_id, "trip_status"] = "stationary"

    if last_value == "pause" or last_value == "end":
        df.loc[df["group"] == max_id, "trip_status"] = "stationary"

    def _adjust_group(group, df):
        # Function to apply to each group.
        # If the group is 'pause' and either the previous group or the next group is 'stationary', change the group to 'stationary'.

        if group["trip_status"].iloc[0] == "pause":
            prev_group_status = (
                df.loc[df["group"] == group.name - 1, "trip_status"].values[-1]
                if group.name > min_id
                else None
            )
            next_group_status = (
                df.loc[df["group"] == group.name + 1, "trip_status"].values[0]
                if group.name < max_id
                else None
            )

            if prev_group_status == "stationary" or next_group_status == "stationary":
                group["trip_status"] = "stationary"

        return group["trip_status"]

    df["trip_status"] = (
        df.groupby("group", as_index=False)
        .apply(lambda x: _adjust_group(x, df))
        .reset_index(level=0, drop=True)
    )  # type: ignore


def _add_ids(
    df: pd.DataFrame, column: str, target_values: list[str], id_column: str
) -> None:
    # Create a mask that changes value every time one of the target values appears after a different value
    mask = df[column].isin(target_values) & (~df[column].shift().isin(target_values))

    # Use cumsum to generate the ID
    df[id_column] = mask.cumsum().astype("UInt16")

    # Set ID to NA for rows that don't match any of the target values
    df.loc[~df[column].isin(target_values), id_column] = pd.NA


def _remove_trips_by_duration(
    df: pd.DataFrame,
    min_duration: timedelta,
) -> None:
    trips = df[
        df["trip_id"].notna() & df["trip_status"].isin(["start", "transport", "end"])
    ]

    # Calculate the duration for each trip.
    trips = trips.groupby(["segment_id", "trip_id"], as_index=False).apply(
        lambda x: x.index.max() - x.index.min()
    )
    trips.rename(columns={None: "duration"}, inplace=True)  # type: ignore

    # Select only the trips that are shorter than the minimum duration.
    removed_trips = trips[trips["duration"] < min_duration][["segment_id", "trip_id"]]

    if not removed_trips.empty:
        # Change rows based on both segment_id and trip_id and set the trip_id and trip_status to NA.
        mask = df.set_index(["segment_id", "trip_id"]).index.isin(
            removed_trips.set_index(["segment_id", "trip_id"]).index
        )
        df.loc[mask, "trip_id"] = pd.NA
        df.loc[mask, "trip_status"] = (
            "stationary"  # FIXME: This should be propably pd.NA, because it is not stationary, but it is not a trip either. Then the two lines below should be removed.
        )
        df.loc[mask, "stationary_id"] = (
            9999  # This will be later changed to correct ID.
        )


def _remove_trips_by_length(
    df: pd.DataFrame,
    crs: CRS,
    min_length: float,
) -> None:
    # Select only the rows that are part of a trip.
    trips = df[
        df["trip_id"].notna() & df["trip_status"].isin(["start", "transport", "end"])
    ][["segment_id", "trip_id", "latitude", "longitude"]]

    # Calculate the distance traveled for each trip.
    trips = trips.groupby(["segment_id", "trip_id"], as_index=False).apply(
        lambda x: get_distance(x, crs)["distance"].sum()
    )
    trips.rename(columns={None: "length"}, inplace=True)  # type: ignore

    # Select only the trips that are shorter than the minimum length.
    removed_trips = trips[trips["length"] < min_length][["segment_id", "trip_id"]]

    if not removed_trips.empty:
        # Change rows based on both segment_id and trip_id and set the trip_id and trip_status to NA.
        mask = df.set_index(["segment_id", "trip_id"]).index.isin(
            removed_trips.set_index(["segment_id", "trip_id"]).index
        )
        df.loc[mask, "trip_id"] = pd.NA
        df.loc[mask, "trip_status"] = (
            "stationary"  # FIXME: This should be propably pd.NA, because it is not stationary, but it is not a trip either. Then the two lines below should be removed.
        )
        df.loc[mask, "stationary_id"] = (
            9999  # This will be later changed to correct ID.
        )


def _change_indoor_trip_to_stationary(df: pd.DataFrame, limit: float) -> str | None:
    environment = df["environment"].value_counts()
    dominant_environment = environment.idxmax()

    if len(environment) >= 2 and dominant_environment == "indoor" and limit:
        total_values = environment.sum()
        dominant_values = environment[dominant_environment]

        if (dominant_values / total_values * 100) <= limit:
            return None

    return dominant_environment  # type: ignore


def _remove_indoor_trips(df: pd.DataFrame, indoor_limit: float):
    # Select only the rows that are part of a trip.
    trips = df[
        df["trip_id"].notna() & df["trip_status"].isin(["start", "transport", "end"])
    ]

    trips = trips.groupby(["segment_id", "trip_id"], as_index=False).apply(
        lambda x: _change_indoor_trip_to_stationary(x, indoor_limit)  # type: ignore
    )

    if not trips.empty:
        trips.rename(columns={None: "environment"}, inplace=True)  # type: ignore
        trips = trips.astype({"environment": "category"})

        removed_trips = trips[trips["environment"] == "indoor"][
            ["segment_id", "trip_id"]
        ]

        # Change rows based on both segment_id and trip_id and set the trip_id and trip_status to NA.
        mask = df.set_index(["segment_id", "trip_id"]).index.isin(
            removed_trips.set_index(["segment_id", "trip_id"]).index
        )
        df.loc[mask, "trip_id"] = pd.NA
        df.loc[mask, "trip_status"] = (
            "stationary"  # FIXME: This should be propably pd.NA, because it is not stationary, but it is not a trip either. Then the two lines below should be removed.
        )
        df.loc[mask, "stationary_id"] = (
            9999  # This will be later changed to correct ID.
        )


def _get_pauses(
    partials: pd.DataFrame,
    crs: CRS,
    pause_radius: float,
    pause_duration: timedelta,
) -> pd.Series:
    # Group by stop_id (unique ID for each trip).
    grouped = partials.groupby("stop_id", as_index=False)

    # Returns a new DataFrame with a 'pause' column.
    if len(grouped) == 1:
        # One trip in segment.
        partials = stop_splitter(partials, crs, pause_radius, pause_duration)  # type: ignore
    else:
        # Multiple trips in segment
        partials = grouped.apply(
            lambda x: stop_splitter(
                x,
                crs,
                pause_radius,
                pause_duration,
            )
        ).reset_index(level=0, drop=True)

    # If there are no pauses, return an empty Series.
    if (~partials).all():
        return pd.Series(name="partial_status")

    partials = pd.DataFrame(partials, columns=["pause"])

    return partials["pause"].astype("boolean")


def _get_trips(
    df: pd.DataFrame,
    crs: CRS,
    stop_radius: float,
    stop_duration: timedelta,
) -> pd.DataFrame:
    # Returns a new DataFrame with a 'stop' column.
    df["stop"] = stop_splitter(
        df,
        crs,
        stop_radius,
        stop_duration,
    )

    # Unique ID for each stop.
    df["stop_id"] = (df["stop"].diff() != 0).cumsum().astype("UInt16")

    # Set the trip status to 'stationary' if the point is a stop, otherwise 'transport'.
    df["trip_status"] = np.where(df["stop"], "stationary", "transport")

    # Creating category column and setting the categories.
    df["trip_status"] = pd.Categorical(
        df["trip_status"], categories=TRIP_STATUS, ordered=False
    )

    return df


def _adjust_trip_statutes(df: pd.DataFrame) -> None:
    # Create a new column 'group' that increments by 1 whenever the 'trip_status' changes
    df["group"] = (df["trip_status"] != df["trip_status"].shift()).cumsum()

    if df["group"].nunique() == 1:
        return

    def _adjust_group(group):
        if len(group) == 1 and group["trip_status"].iloc[0] == "transport":
            group["trip_status"] = "pause"

        return group["trip_status"]

    df["trip_status"] = (
        df.groupby("group", as_index=False)
        .apply(lambda x: _adjust_group(x))
        .reset_index(level=0, drop=True)
    )  # type: ignore


def _get_segment_trips(
    df: pd.DataFrame,
    crs: CRS,
    sample_rate: timedelta,
    stop_radius: float,
    stop_duration: timedelta,
    pause_radius: float | None = None,
    pause_duration: timedelta | None = None,
    min_distance: float | None = None,
):
    # Filter out points that are too close to each other.
    if min_distance:
        min_distance = _convert_distance_parameter(min_distance, sample_rate)
        filtered = min_distance_filter(df, crs, min_distance)
        df = df[filtered]

    # Get the trips from the DataFrame.
    df = _get_trips(df, crs, stop_radius, stop_duration)
    partials = df[~df["stop"]]

    # Get the pauses from the DataFrame.
    if (not pause_radius and not pause_duration) or partials.empty:
        pauses = pd.Series(name="partial_status")
    else:
        if not pause_radius:
            pause_radius = stop_radius

        if not pause_duration:
            pause_duration = stop_duration

        pauses = _get_pauses(
            partials[["latitude", "longitude", "stop_id"]],
            crs,
            pause_radius,
            pause_duration,
        )

    # Merge the pauses with the trips if there are any.
    if not pauses.empty:
        df = df.join(
            pauses,
            how="left",
            validate="one_to_one",
        )
        # Set the trip status to 'pause' if the point is a pause, otherwise it stays transport/stationary.
        df.loc[df["pause"], "trip_status"] = "pause"
        _adjust_trip_statutes(df)

        # Change the pause status to 'stationary' if necessary, so if pause follows a stationary point, it is also stationary.
        _adjust_stationary_statutes(df)

        if (df["trip_status"] == "pause").all():
            df["trip_status"] = "stationary"
            df["trip_id"] = pd.NA

    # Fix the start and end of trips and locations.
    _add_ids(df, "trip_status", ["pause", "transport"], "trip_id")
    _add_ids(
        df,
        "trip_status",
        ["pause", "stationary"],
        "stationary_id",
    )

    # Add start and end boundaries to trips. Overlapping trips/pauses/stationaries.
    # _add_boundaries(df, "trip_id", "trip_status")

    cols = ["trip_status", "trip_id", "stationary_id"]
    if "environent" in df.columns:
        cols.append("environment")

    return df[cols]


def detect_trips(
    df: pd.DataFrame,
    sample_rate: timedelta,
    crs: CRS,
    gap_duration: timedelta,
    stop_radius: float,
    stop_duration: timedelta,
    pause_radius: float | None,
    pause_duration: timedelta | None,
    min_duration: timedelta | None,
    min_length: float | None,
    min_distance: float | None,
    indoor_limit: float | None,
) -> pd.DataFrame:
    # TODO: Sometimes short trips are between pauses, and it seems like a stupid thing. So they should be removed but then the pauses might be the whole trip etc. So it is a bit tricky.
    if gap_duration <= sample_rate:
        raise ValueError("Gap duration must be greater than the sampling rate.")

    if stop_duration <= sample_rate:
        raise ValueError("Stop duration must be greater than the sampling rate.")

    if pause_duration and stop_duration <= pause_duration:
        raise ValueError("Stop duration must be greater than pause duration.")

    if min_duration and min_duration <= sample_rate:
        raise ValueError("Minimum duration must be greater than the sampling rate.")

    if Column.ENVIRONMENT not in df.columns and indoor_limit:
        raise ValueError(
            errors["columns_not_exists"].format(missing_columns=[Column.ENVIRONMENT])
        )

    cols = {Column.LATITUDE: "latitude", Column.LONGITUDE: "longitude"}
    if Column.ENVIRONMENT in df.columns:
        cols[Column.ENVIRONMENT] = "environment"

    df = df[list(cols.values())].copy()
    df.rename(columns=cols, inplace=True)
    df = df.loc[df[["latitude", "longitude"]].notnull().all(axis=1)]

    if df.empty:
        raise ValueError(errors["empty_df"])

    df["segment_id"] = gap_splitter(df, min_duration=gap_duration)

    df = (
        df.groupby("segment_id")
        .apply(
            lambda x: _get_segment_trips(
                x,
                crs=crs,
                sample_rate=sample_rate,
                stop_radius=stop_radius,
                stop_duration=stop_duration,
                pause_radius=pause_radius,
                pause_duration=pause_duration,
                min_distance=min_distance,
            )
        )
        .reset_index(level=0, drop=False)
    )  # type: ignore

    df["trip_status"] = pd.Categorical(
        df["trip_status"], categories=TRIP_STATUS, ordered=False
    )

    # Remove trips that are too short (duration).
    if min_duration:
        _remove_trips_by_duration(df, min_duration)

    # Remove trips that are too short (length).
    if min_length:
        _remove_trips_by_length(df, crs, min_length)

    if Column.ENVIRONMENT in df.columns and indoor_limit:
        # TODO: Should be this set outside of the function? And maybe just annotated if the trip is indoor or not, so researchers can exclude indoor trips and say that they are stationary.
        _remove_indoor_trips(df, indoor_limit)

    df = df[df["trip_status"].notna()]
    trip_mask = df["trip_id"].notna()
    stationary_mask = df["stationary_id"].notna()

    # Renumbers the trip IDs to be unique across all segments.
    df.loc[trip_mask, "trip_id"] = (
        pd.factorize(
            df.loc[trip_mask, "segment_id"].astype(str)
            + "_"
            + df.loc[trip_mask, "trip_id"].astype(str)
        )[0]
        + 1
    )

    # Renumbers the stationary IDs to be unique across all segments.
    df["stationary_id"] = (
        df["stationary_id"].isna().astype(int).diff().ne(0).cumsum()
    ).where(stationary_mask)

    df.loc[stationary_mask, "stationary_id"] = (
        pd.factorize(
            df.loc[stationary_mask, "segment_id"].astype(str)
            + "_"
            + df.loc[stationary_mask, "stationary_id"].astype(str)
        )[0]
        + 1
    )

    df = df.astype(
        {
            "segment_id": "UInt16",
            "stationary_id": "UInt16",
        }
    )

    return df[
        [
            "segment_id",
            "trip_status",
            "trip_id",
            "stationary_id",
        ]
    ]
