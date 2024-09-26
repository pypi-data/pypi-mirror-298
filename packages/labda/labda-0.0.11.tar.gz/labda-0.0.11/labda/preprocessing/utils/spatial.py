from zoneinfo import ZoneInfo

import geopandas as gpd
import pandas as pd
from pyproj import CRS
from timezonefinder import TimezoneFinder

from ...logs import errors
from ...structure.validation import Column
from .common import columns_checker, fix_columns

DEFAULT_CRS = CRS.from_string("EPSG:4326")


def df_to_gdf(
    df: pd.DataFrame,
    crs: CRS | None = None,
    geometry: str | None = None,
) -> gpd.GeoDataFrame:
    """
    Converts a DataFrame to a GeoDataFrame by creating a geometry column from latitude and longitude columns.

    Args:
        df (pd.DataFrame): The DataFrame to be converted.
        crs (CRS | None, optional): The coordinate reference system (CRS) of the GeoDataFrame. Defaults to None.

    Returns:
        gpd.GeoDataFrame: The converted GeoDataFrame.
    """

    if crs is None:
        crs = DEFAULT_CRS

    if geometry:
        columns_checker(df, [geometry], True)
        gdf = gpd.GeoDataFrame(
            df,
            geometry=str(geometry),
            crs=crs,
        )  # type: ignore
    else:
        columns_checker(df, [Column.LATITUDE, Column.LONGITUDE], True)
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df[Column.LONGITUDE], df[Column.LATITUDE]),
            crs=crs,
        )  # type: ignore
        gdf.drop(columns=[Column.LATITUDE, Column.LONGITUDE], inplace=True)

    return gdf


def gdf_to_df(
    gdf: gpd.GeoDataFrame,
    geometry: str | None = None,
) -> pd.DataFrame:
    """
    Converts a GeoDataFrame to a DataFrame by extracting the latitude and longitude
    coordinates from the geometry column. The geometry column is dropped in the process.

    Args:
        gdf (gpd.GeoDataFrame): The input GeoDataFrame.

    Returns:
        pd.DataFrame: The converted DataFrame with latitude and longitude columns.
    """

    df = pd.DataFrame(gdf)

    if not geometry:
        df[Column.LATITUDE] = gdf.geometry.y
        df[Column.LONGITUDE] = gdf.geometry.x
        df.drop(columns=["geometry"], inplace=True)
        df = df.astype({Column.LATITUDE: "Float64", Column.LONGITUDE: "Float64"})

    return df


def get_crs(df: pd.DataFrame, crs: CRS | None, geometry: str | None = None) -> CRS:
    """
    Guesses the coordinate reference system (CRS) of a DataFrame containing spatial data. The CRS is estimated using the WGS84 ellipsoid.

    Args:
        df (pd.DataFrame): The DataFrame containing spatial data.

    Returns:
        CRS: The estimated CRS of the DataFrame.
    """

    gdf = df_to_gdf(df, crs, geometry)  # type: ignore
    estimated_crs = gdf.geometry.estimate_utm_crs()

    return estimated_crs


def change_crs(
    df: pd.DataFrame,
    source: CRS,
    target: CRS,
    geometry: str | None = None,
) -> pd.DataFrame:
    gdf = df_to_gdf(df, source, geometry)
    gdf.to_crs(target, inplace=True)
    df = gdf_to_df(gdf, geometry)

    df = fix_columns(df)

    return df


def get_timezone(
    df: pd.DataFrame,
    crs: CRS,
    sample: int = 10,
    limit: float = 0.8,
    geometry: str | None = None,
) -> ZoneInfo:
    if not geometry:
        columns_checker(df, [Column.LATITUDE, Column.LONGITUDE], True)
        temp = df[df[Column.LATITUDE].notna() & df[Column.LONGITUDE].notna()]
    else:
        columns_checker(df, [geometry], True)
        temp = df_to_gdf(df[df[geometry].notna()], crs, geometry)
        temp = pd.concat([temp, temp.get_coordinates()], axis=1)
        temp.rename(columns={"y": Column.LATITUDE, "x": Column.LONGITUDE}, inplace=True)

    if crs != DEFAULT_CRS:
        temp = change_crs(temp, crs, DEFAULT_CRS)

    temp = temp.sample(sample)

    tz_finder = TimezoneFinder()
    temp["timezone"] = temp.apply(
        lambda row: tz_finder.timezone_at(
            lat=row[Column.LATITUDE], lng=row[Column.LONGITUDE]
        ),  # type: ignore
        axis=1,
    )

    timezones = temp["timezone"].value_counts()
    timezone = timezones.idxmax()

    n = len(temp)
    count = timezones.loc[timezone]
    percentage = count / n

    if percentage < limit:
        raise ValueError(
            errors["timezone_frequency"].format(
                limit=limit * 100, frequency=percentage * 100
            )
        )

    return ZoneInfo(timezone)  # type: ignore


def get_crs_units(crs: CRS) -> str:
    units = crs.axis_info[0].unit_name  # type: ignore

    return units
