import pandas as pd
from pyproj import CRS

from ..utils.spatial import df_to_gdf, get_crs_units


def min_distance_filter(
    df: pd.DataFrame,
    crs: CRS,
    min_distance: float,
) -> pd.Series:
    gdf = df_to_gdf(df, crs=crs)
    units = get_crs_units(crs)

    if units != "metre":
        raise ValueError(f"Unsupported unit: {units}.")

    keep_pts = [gdf.index[0]]  # Keep first point, always.
    prev_pt = gdf.geometry.iloc[0]

    for idx, pt in gdf.geometry.items():
        dist = pt.distance(prev_pt)
        if dist >= min_distance:
            keep_pts.append(idx)
            prev_pt = pt

    keep_pts.append(gdf.index[-1])

    filtered = pd.Series(False, index=df.index)
    filtered[keep_pts] = True

    return filtered
