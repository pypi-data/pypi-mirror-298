from datetime import timedelta
from typing import Any

import geopandas as gpd
import osmnx as ox
import pandas as pd
import shapely
from pandas import json_normalize
from pyproj import CRS

from ...preprocessing.utils.spatial import df_to_gdf, gdf_to_df


def _get_polygon(s: pd.Series, buffer):
    return s.union_all().convex_hull.buffer(buffer)


def _get_boundaries(
    gdf: gpd.GeoDataFrame,
    crs: CRS,
    buffer: float,
) -> shapely.MultiPolygon:
    boundaries = gdf.groupby("stationary_id")["geometry"].apply(
        lambda x: _get_polygon(x, buffer), include_groups=False
    )
    boundaries = boundaries.set_crs(crs).to_crs(epsg=4326).union_all()

    return boundaries


def _get_features(
    boundaries: shapely.MultiPolygon,
    tags: dict[str, Any],
    crs: CRS,
    nodes: bool = False,
) -> gpd.GeoDataFrame:
    gdf = ox.features_from_polygon(boundaries, tags)  # type: ignore
    gdf.to_crs(crs, inplace=True)
    gdf.reset_index(level=0, inplace=True)

    if not nodes:
        gdf = gdf[gdf["element"] == "way"]

    if gdf.empty:
        raise ValueError("No features found.")

    return gdf  # type: ignore


def _get_stationary(df: pd.DataFrame) -> pd.Series:
    geometry = df.geometry.union_all()
    duration = df.index.max() - df.index.min()

    if isinstance(geometry, shapely.geometry.Point):
        geometry = shapely.geometry.MultiPoint([geometry])

    return pd.Series({"geometry": geometry, "duration": duration})


def _get_stationaries(
    df: pd.DataFrame,
    crs: CRS,
    pause: bool,
) -> gpd.GeoDataFrame:
    rule = df["stationary_id"].notna()

    if not pause:
        rule = rule & (df["trip_status"] != "pause")

    gdf = df_to_gdf(df[rule], crs)
    gdf = gdf.groupby("stationary_id").apply(
        lambda x: _get_stationary(x),  # type: ignore
        include_groups=False,
    )

    if gdf.empty:
        raise ValueError("No stationary points found.")

    gdf["max_points"] = gdf["geometry"].apply(lambda x: len(x.geoms))

    return gdf  # type: ignore


def _check_points(polygon: pd.DataFrame, points: gpd.GeoDataFrame) -> bool:
    return points.intersects(polygon).sum()


def _detect_intersections(
    geometry: shapely.geometry.MultiPoint,
    gdf: gpd.GeoDataFrame,
    crs: CRS,
) -> list[dict[str, Any]]:
    polygon = geometry.convex_hull
    points = gpd.GeoDataFrame(geometry=[geometry], crs=crs).explode()  # type: ignore

    gdf = gdf[["geometry_buffer"]].copy()  # type: ignore
    gdf["overlay"] = gdf.intersects(polygon)  # type: ignore
    gdf = gdf[gdf["overlay"]]  # type: ignore
    gdf["points"] = gdf.loc[gdf.index].geometry.apply(_check_points, points=points)
    gdf.index.name = "osm_id"
    gdf.reset_index(inplace=True)

    return gdf[["osm_id", "points"]].to_dict(orient="records")  # type: ignore


def _get_overlay_features(
    stationaries: gpd.GeoDataFrame,
    features: gpd.GeoDataFrame,
    crs: CRS,
) -> pd.DataFrame:
    overlays = stationaries["geometry"].apply(
        lambda x: _detect_intersections(x, features, crs)
    )
    overlays = overlays.explode()  # type: ignore
    indexes = overlays.index
    overlays = json_normalize(overlays)  # type: ignore
    overlays = overlays.set_index(indexes)
    overlays = overlays.join(stationaries)

    return overlays


def get_features(
    df: pd.DataFrame,
    crs: CRS,
    tags: dict[str, bool | str | list[str]],
    buffer: float,
) -> pd.DataFrame:
    # This function is only for stationary, not tested for trips (everything)
    df = df[df["stationary_id"].notna()]

    gdf = df_to_gdf(df, crs)
    boundaries = _get_boundaries(gdf, crs, buffer)  # type: ignore
    features = _get_features(boundaries, tags, crs)

    return pd.DataFrame(features)


def detect_locations(
    df: pd.DataFrame,
    features: pd.DataFrame,
    crs: CRS,
    duration: timedelta | None = None,
    limit: float | None = None,
    buffer: float | None = None,
) -> pd.DataFrame:
    # Also, only for stationary. Not tested for trips.

    stationaries = _get_stationaries(df, crs, False)
    features = df_to_gdf(features, crs, "geometry")

    if buffer:
        features["geometry_buffer"] = features["geometry"].buffer(buffer)  # type: ignore
    else:
        features["geometry_buffer"] = features["geometry"]
    features.set_geometry("geometry_buffer", inplace=True)

    overlays = _get_overlay_features(stationaries, features, crs)

    limit_rule = True
    duration_rule = True

    if limit:
        limit_rule = (100 / overlays["max_points"]) * (
            overlays["points"]
        ) >= limit * 100

    if duration:
        duration_rule = overlays["duration"] >= duration

    overlays["valid"] = limit_rule & duration_rule

    features.rename(columns={"geometry": "osm_geometry"}, inplace=True)
    locations = overlays.merge(
        features, left_on="osm_id", right_index=True, how="left", validate="many_to_one"
    )

    locations.loc[locations["building"] == "yes", "building"] = "building"
    cols = [
        "max_points",
        "points",
        "valid",
        "duration",
        "geometry",
        "osm_geometry",
        "osm_id",
        "name",
        "building",
        "building:levels",
        "shelter_type",
        "amenity",
        "shop",
        # "wikidata",
    ]

    # Fun stuff - remove it later
    # fun_stuff = ["cuisine", "takeaway", "outdoor_seating"]
    # cols = cols + fun_stuff
    # locations["cuisine"] = locations["cuisine"].apply(
    #     lambda x: x.split(";") if isinstance(x, str) else x
    # )

    locations = locations[cols]
    # locations.rename(columns={"wikidata": "wiki_id"}, inplace=True)

    return locations


def _get_location_summary(df: pd.DataFrame) -> pd.Series:
    row = df.iloc[0]

    return pd.Series(
        {
            "stationary_id": row["stationary_id"],
            "max_points": df["max_points"].sum(),
            "points": df["points"].sum(),
            "valid": row["valid"],
            "duration": df["duration"].sum(),
            "geometry": df["geometry"].union_all(),
            "osm_geometry": row["osm_geometry"],
            "name": row["name"],
            "building": row["building"],
            "building:levels": row["building:levels"],
            "shelter_type": row["shelter_type"],
            "amenity": row["amenity"],
            "shop": row["shop"],
            # "wiki_id": row["wiki_id"],
            # # Fun stuff
            # "cuisine": row["cuisine"],
            # "takeaway": row["takeaway"],
            # "outdoor_seating": row["outdoor_seating"],
        }
    )


def get_location_summaries(
    df: pd.DataFrame,
    crs: CRS,
    only_valid: bool = False,
) -> pd.DataFrame:
    if only_valid:
        df = df[df["valid"]]

    gdf = df_to_gdf(df, crs, geometry="geometry").reset_index()
    summaries = gdf.groupby("osm_id").apply(_get_location_summary, include_groups=False)  # type: ignore
    summaries = summaries.reset_index().set_index("stationary_id")
    summaries = gdf_to_df(summaries, geometry="geometry")  # type: ignore

    return summaries
