from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:
    from ...structure import SampleRate

import pandas as pd
from agcounts.extract import get_counts as ag_counts

from ...preprocessing.utils.common import columns_checker
from ...structure.validation import Column, Placement


def _scale_cut_points(
    cut_points: dict[str, Any],
    sample_rate: "SampleRate",
) -> tuple[dict[str, Any], str | None]:
    counts_sr = cut_points["sample_rate"]  # type: SampleRate

    counts_sr_sec = counts_sr.to_seconds()
    data_sr_sec = sample_rate.to_seconds()

    if counts_sr_sec != data_sr_sec:
        scaled = f"Cut points scaled from sample rate {counts_sr} to {sample_rate}."
        coeff = counts_sr_sec / data_sr_sec

        for cp in cut_points["cut_points"]:
            cp["max"] = cp["max"] / coeff
    else:
        scaled = None

    return cut_points, scaled


def _apply_cut_points(
    df: pd.DataFrame,
    on: Column,
    cut_points: dict[str, Any],
) -> pd.Series:
    # Extract min and max values from cut_points
    bins = [-float("inf")]
    bins += [cp["max"] for cp in cut_points["cut_points"]]

    # Extract names from cut_points
    labels = [cp["name"] for cp in cut_points["cut_points"]]

    # Apply cut points
    return pd.cut(df[on], bins=bins, labels=labels)


def _check_placement(
    source: Placement | None,
    target: Placement | None,
) -> str | None:
    if (not source or not target) or source != target:
        return f"Placement mismatch, consider checking the data (cut points were based on {source}, but data is from {target})."


def detect_activity_intensity_from_counts(
    df: pd.DataFrame,
    cut_points: dict[str, Any],
    sample_rate: "SampleRate",
    placement: Placement | None,
) -> tuple[pd.Series, list[str | None]]:
    required_column = cut_points["required_data"]
    columns_checker(df, [required_column], exists=True)

    source_placement = cut_points["placement"]
    placement_check = _check_placement(source_placement, placement)

    cut_points, scaled = _scale_cut_points(cut_points, sample_rate)

    counts = _apply_cut_points(df, required_column, cut_points)

    return counts, [scaled, placement_check]


def detect_counts_from_raw(
    df: pd.DataFrame,
    source: "SampleRate",
    target: "SampleRate",
) -> pd.DataFrame:
    source_hz = source.to_hz()
    target_s = target.to_seconds()

    acc_cols = [Column.ACC_X, Column.ACC_Y, Column.ACC_Z]
    columns_checker(df, acc_cols, exists=True)  # type: ignore
    df = df[acc_cols]

    if source_hz not in [30, 40, 50, 60, 70, 80, 90, 100]:
        raise ValueError(
            f"Invalid source sample rate: {source}. Must be one of 30, 40, 50, 60, 70, 80, 90, 100 hz."
        )

    if not target_s.is_integer():
        raise ValueError(
            f"Invalid target sample rate: {target}. Must be a full second value."
        )

    counts = ag_counts(df.astype(np.float32).to_numpy(), int(source_hz), int(target_s))  # type: ignore

    return pd.DataFrame(counts)
