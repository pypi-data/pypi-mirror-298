from json import tool
from pathlib import Path

import geopandas as gpd
import pandas as pd
import pydeck as pdk
from PIL import ImageColor
from pyproj import CRS
from shapely import LineString, Point

from ..preprocessing.utils.spatial import df_to_gdf
from ..processing.spatial.timeline import get_timeline

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


POINT_RADIUS = 16  # 10
LINE_WIDTH = 8  # 5
OPACITY = 0.5

COLORS = [
    "#FF0000",
    "#FF8700",
    "#FFD300",
    "#DEFF0A",
    "#A1FF0A",
    "#0AFF99",
    "#0AEFFF",
    "#147DF5",
    "#580AFF",
    "#BE0AFF",
]  # TODO: There needs to be much more colors, infinity number of colors almost.


def _update_trip_ids(df: pd.DataFrame) -> pd.DataFrame:
    # FIXME: THIS IS IMPORTANT FEATURE, SHOULD BE MOVED TO UTILS PROBABLY
    forward_ids = df["trip_id"].shift(1)
    backward_ids = df["trip_id"].shift(-1)
    id = forward_ids.combine_first(backward_ids)

    forward_mode = df["trip_mode"].shift(1)
    backward_mode = df["trip_mode"].shift(-1)
    mode = forward_mode.combine_first(backward_mode)

    new = id.to_frame()
    new["trip_status"] = df["trip_status"]
    new["trip_mode"] = mode
    new.loc[new["trip_mode"].notna(), "trip_status"] = "transport"

    return new


def update_trips_ids(df: pd.DataFrame) -> pd.DataFrame:
    df[["trip_id", "trip_status", "trip_mode"]] = (
        df.groupby("segment_id")
        .apply(_update_trip_ids, include_groups=False)
        .reset_index(level=0, drop=True)
    )

    return df


def get_color(color: str) -> tuple[int]:
    return ImageColor.getcolor(color, "RGB")  # type: ignore


def _get_unique_random_color(
    df: pd.DataFrame,
    column: str,
    colors: list[str],
    null: str | None = None,
) -> pd.Series:
    unique = df[column].unique()
    color_map = dict(zip(unique, colors))
    series = df[column].map(color_map, na_action="ignore")

    if null:
        series = series.cat.add_categories(null)
        series = series.fillna(COLORS[5])

    return series


def _get_status(row) -> str:
    trip_id = row["trip_id"]
    stationary_id = row["stationary_id"]
    mode = row["trip_mode"]

    match row["trip_status"]:
        case "trip":
            text = f"Trip {int(trip_id)} ({mode})"
        case "pause":
            text = f"Trip {int(trip_id)} (Pause {int(stationary_id)})"
        case "stationary":
            text = f"Stationary {int(stationary_id)}"
        case _:
            text = "Unknown"

    return text


def _get_transport_color(row) -> str:
    match row["trip_mode"]:
        case "walk/run":
            color = COLORS[4]
        case "bicycle":
            color = COLORS[3]
        case "vehicle":
            color = COLORS[1]
        case _:
            color = COLORS[5]

    return color


def get_points_layer(
    gdf: gpd.GeoDataFrame,
    color: str | tuple[int],
    pickable: bool = True,
) -> pdk.Layer:
    return pdk.Layer(
        "GeoJsonLayer",
        gdf,
        stroked=False,
        filled=True,
        get_position="geometry.coordinates",
        get_fill_color=color,
        get_line_color=color,
        get_line_width=LINE_WIDTH,
        opacity=OPACITY,
        pickable=pickable,
        auto_highlight=True,
        get_radius=POINT_RADIUS,  # Radius is in meters
    )


def get_contexts_layer(contexts: gpd.GeoDataFrame) -> pdk.Layer:
    contexts["duration"] = "TODO..."  # TODO: Duration based on if start/end
    contexts["distance"] = "TODO..."  # TODO: Area with unit or radius
    contexts["title"] = (
        contexts["name"].str.capitalize()
        + " (Priority:"
        + contexts["priority"].astype(str)
        + ")"
    )

    contexts["start"] = contexts["start"].dt.strftime(DATETIME_FORMAT)
    contexts["end"] = contexts["end"].dt.strftime(DATETIME_FORMAT)

    return pdk.Layer(
        "GeoJsonLayer",
        contexts,
        filled=False,
        get_position="geometry.coordinates",
        get_line_color=get_color("#FFFFFF"),
        get_line_width=LINE_WIDTH,
        opacity=1,
        pickable=True,
        auto_highlight=True,
    )


def get_tooltip(row: pd.Series, type: str) -> str | None:
    match type:
        case "points":
            text = f"""
        <strong>Datetime:</strong> {row.name.strftime(DATETIME_FORMAT)}<br><br>
        <strong>Coordinates:</strong> {row["geometry"].x:.6f}, {row["geometry"].y:.6f}
        """
        case "contexts":
            text = f"""
        <strong>Context:</strong> {row["name"].capitalize()}<br><br>
        <strong>Area:</strong> {row["area"]:,.2f}
        """
        case "locations":
            text = f"""
        <strong>OSM:</strong> {int(row["osm_id"])}
        """
        case "trips":
            text = f"""
        <strong>Trip:</strong> {row["trip_id"]} ({str(row["trip_status"]).capitalize()}, {str(row["trip_mode"]).capitalize()})<br>
        <strong>Start:</strong> {row["start"].strftime(DATETIME_FORMAT)}<br>
        <strong>End:</strong> {row["end"].strftime(DATETIME_FORMAT)}<br>
        <strong>Duration:</strong> {row["duration"]}
        """
        case "lines":
            text = None

    return text


def plot(
    df: pd.DataFrame,
    contexts: pd.DataFrame,
    locations: pd.DataFrame,
    crs: CRS,
    objects: list[str] | None,
    center: Point | None,
    zoom: int | None,
    path: Path | str | None = None,
) -> str:
    gdf = df_to_gdf(df, crs)
    gdf.to_crs(epsg=4326, inplace=True)

    if not isinstance(center, Point):
        center = gdf.geometry.union_all().centroid

    if objects is None:
        objects = []

    layers = []

    if "lines" in objects:
        line = LineString(gdf["geometry"])
        line = gpd.GeoDataFrame(geometry=[line], crs=gdf.crs)  # type: ignore
        layers.append(get_points_layer(line, get_color(COLORS[5]), pickable=False))
        # objects.append("points")

    if "points" in objects and "points+contexts" not in objects:
        color = get_color(COLORS[5])
        gdf["tooltip"] = gdf.apply(lambda x: get_tooltip(x, "points"), axis=1)
        layers.append(get_points_layer(gdf, color))

    if "points+contexts" in objects:
        gdf["color"] = _get_unique_random_color(gdf, "context", COLORS, null=COLORS[5])
        gdf["color"] = gdf.apply(lambda x: get_color(x["color"]), axis=1)
        gdf.sort_values("context", inplace=True, na_position="first")
        layers.append(get_points_layer(gdf, "color"))

    if "contexts" in objects and not contexts.empty:
        contexts = gpd.GeoDataFrame(contexts, crs=crs)  # type: ignore
        contexts["area"] = contexts.area
        contexts.to_crs(epsg=4326, inplace=True)
        contexts["tooltip"] = contexts.apply(
            lambda x: get_tooltip(x, "contexts"), axis=1
        )
        layers.append(get_contexts_layer(contexts))

    if "locations" in objects and not locations.empty:
        # locations["title"] = locations["osm_id"]
        # locations["duration"] = locations["duration"].astype(str)
        locations = gpd.GeoDataFrame(locations, crs=crs, geometry="osm_geometry")  # type: ignore
        locations.to_crs(epsg=4326, inplace=True)
        locations["tooltip"] = locations.apply(
            lambda x: get_tooltip(x, "locations"), axis=1
        )
        layers.append(get_points_layer(locations, get_color(COLORS[0])))

    if "trips" in objects or "trips+transport" in objects or "stationary" in objects:
        if "trips" in objects or "trips+transport" in objects:
            # df = update_trips_ids(df)
            timeline = get_timeline(df, crs)
            gdf = df_to_gdf(timeline, crs, "geometry")
            gdf.to_crs(epsg=4326, inplace=True)

            trips_points = gdf[gdf["trip_status"].isin(["trip", "pause"])].copy()  # type: ignore
            trips_points.loc[trips_points["trip_status"] == "pause", "color"] = COLORS[
                7
            ]

            if "trips+transport" in objects:
                trips_points.loc[trips_points["trip_mode"].notna(), "color"] = (
                    trips_points.apply(_get_transport_color, axis=1)
                )
            else:
                trips_points.loc[trips_points["trip_status"] == "trip", "color"] = (
                    COLORS[5]
                )

            trips_points["color"] = trips_points.apply(
                lambda x: get_color(x["color"]), axis=1
            )
            trips_points["tooltip"] = trips_points.apply(
                lambda x: get_tooltip(x, "trips"), axis=1
            )
            layers.append(get_points_layer(trips_points, "color"))  # type: ignore

        if "stationary" in objects:
            timeline = get_timeline(df, crs)
            gdf = df_to_gdf(timeline, crs, "geometry")
            gdf.to_crs(epsg=4326, inplace=True)
            locations_points = gdf.loc[gdf["trip_status"] == "stationary"]  # type: ignore
            layers.append(get_points_layer(locations_points, get_color(COLORS[0])))

    # Set the viewport location
    view_state = pdk.ViewState(longitude=center.x, latitude=center.y, zoom=zoom)  # type: ignore

    tooltip = {
        "html": "{tooltip}",
    }

    # Render
    render = pdk.Deck(layers=layers, initial_view_state=view_state, tooltip=tooltip)  # type: ignore
    return render.to_html(filename=path)  # type: ignore
