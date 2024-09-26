from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...structure import SampleRate

import pandas as pd

from ...preprocessing.utils.common import columns_checker
from ...structure.validation import Placement
from ..bouts import get_bouts


def _scale_cut_points(
    params: dict[str, Any],
    sample_rate_from: "SampleRate",
    sample_rate_to: "SampleRate",
    cut_points: list[str],
) -> tuple[dict[str, Any], str | None]:
    sr_from = sample_rate_from.to_seconds()
    sr_to = sample_rate_to.to_seconds()

    if sr_from != sr_to:
        scaled = f"Cut points scaled from sample rate {sample_rate_from} to {sample_rate_to}."
        coeff = sr_from / sr_to

        for key in cut_points:
            params[key] = params[key] / coeff
    else:
        scaled = None

    return params, scaled


def _check_placement(
    source: Placement | None,
    target: Placement | None,
) -> str | None:
    # FIXME: Duplicated functions, also in counts.py
    if (not source or not target) or source != target:
        return f"Placement mismatch, consider checking the data (cut points were based on {source}, but data is from {target})."


def detect_wear(
    df: pd.DataFrame,
    cut_points: dict[str, Any],
    sample_rate: "SampleRate",
    placement: Placement | None,
) -> tuple[pd.Series, list[str | None]]:
    required_data = cut_points["required_data"]
    columns_checker(df, [required_data], True)

    source_placement = cut_points["placement"]
    placement_check = _check_placement(source_placement, placement)

    sample_rate_from = cut_points["sample_rate"]  # type: SampleRate

    values = [
        "bout_min_value",
        "bout_max_value",
        "artefact_min_value",
        "artefact_max_value",
    ]

    params = cut_points["params"]
    params, scaled = _scale_cut_points(params, sample_rate_from, sample_rate, values)

    wear = get_bouts(df[required_data], sample_rate.to_timedelta(), **params)

    return ~wear, [scaled, placement_check]
