from collections import deque
from datetime import timedelta

import pandas as pd
from pyproj import CRS

from ..utils.spatial import df_to_gdf, get_crs_units


def stop_splitter(
    df: pd.DataFrame,
    crs: CRS,
    max_radius: float,
    min_duration: timedelta,
) -> pd.Series:
    # TODO: How to handle NA values, maybe just filter to have only valid points (with coordinates).
    # TODO: Are NA values dropped when transforming to GeoDataFrame? If not, let's filter it out.
    gdf = df_to_gdf(df, crs=crs)
    units = get_crs_units(crs)

    if units != "metre":
        raise ValueError(f"Unsupported unit: {units}.")

    splitted = pd.Series(False, index=df.index)

    buffer = deque()
    for dt in gdf.index:
        buffer.append(dt)
        if dt - buffer[0] >= min_duration:
            selected_rows = gdf.loc[buffer[0] : dt]
            centroid = selected_rows.geometry.unary_union.centroid

            for row in selected_rows.geometry:
                distance = centroid.distance(row)
                if distance > max_radius:
                    break
            else:
                splitted.loc[selected_rows.index] = True

            buffer.popleft()

    return splitted
