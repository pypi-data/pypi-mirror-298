from datetime import datetime
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..structure.contexts import Context

import geopandas as gpd
import pandas as pd


def _get_spatial_context(gdf: gpd.GeoDataFrame, geometry) -> pd.Series:
    rows = gdf.within(geometry, align=False)
    return rows


def _get_temporal_context(
    df: pd.DataFrame,
    start: datetime | None,
    end: datetime | None,
) -> pd.Series:
    # rows = pd.Series((df.index >= start) & (df.index < end), index=df.index)
    if pd.notna(start) and pd.notna(end):
        filter = (df.index >= start) & (df.index < end)
    elif pd.notna(start):
        filter = df.index >= start
    elif pd.notna(end):
        filter = df.index < end
    else:
        filter = pd.Series(False, index=df.index)

    rows = pd.Series(filter, index=df.index)
    return rows


def detect_priority_contexts(df: pd.DataFrame, contexts: list["Context"]) -> pd.Series:
    contexts = sorted(contexts, key=lambda c: c.priority)
    series = pd.Series(name="context", index=df.index, dtype=str)

    for context in contexts:
        series.loc[df.index.isin(context.indexes)] = context.name

    return series.astype("category")


def detect_contexts(
    gdf: gpd.GeoDataFrame, contexts: gpd.GeoDataFrame
) -> list[dict[str, Any]]:
    if gdf.crs != contexts.crs:
        raise ValueError("The GeoDataFrames must have the same CRS.")

    results = []

    for context in contexts.itertuples():
        context = context._asdict()  # type: ignore
        del context["Index"]
        del context["subject_id"]

        name = context.get("context")
        geometry = context.get("geometry")
        start = context.get("start")
        end = context.get("end")

        spatial = pd.Series()
        temporal = pd.Series()

        if geometry:
            spatial = _get_spatial_context(gdf, geometry)

        if pd.notna(start) or pd.notna(end):
            temporal = _get_temporal_context(gdf, start, end)

        if not spatial.empty and not temporal.empty:
            indexes = spatial & temporal
        elif not spatial.empty:
            indexes = spatial
        elif not temporal.empty:
            indexes = temporal

        indexes.name = name
        context["indexes"] = indexes[indexes].index

        results.append(context)

    return results
