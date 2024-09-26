from datetime import timedelta

import pandas as pd


def _get_bouts(bouts: pd.DataFrame, duration: timedelta) -> bool:
    if (bouts.index[-1] - bouts.index[0]) >= duration:
        return True

    return False


def _get_artefacts(
    artefacts: pd.DataFrame,
    duration: timedelta,
    bouts: timedelta,
    df: pd.DataFrame,
) -> bool:
    first = artefacts.index[0]
    last = artefacts.index[-1]

    if (last - first) <= duration:
        if bouts:
            before = df["bout"].loc[first - bouts : first].iloc[:-1]
            before = before.all()

            if before:
                after = df["bout"].loc[last : last + bouts].iloc[1:]
                after = after.all()

                if after:
                    return True
        else:
            return True

    return False


def get_bouts(
    series: pd.Series,
    sample_rate: timedelta,
    bout_min_duration: timedelta,
    bout_min_value: float,
    bout_max_value: float,
    artefact_max_duration: timedelta,
    artefact_between_duration: timedelta,
    artefact_min_value: float,
    artefact_max_value: float,
) -> pd.Series:
    series = series.resample(sample_rate).asfreq()
    df = pd.DataFrame(index=series.index)
    df["bout"] = (series >= bout_min_value) & (series <= bout_max_value)
    df["bout_id"] = (df["bout"] != df["bout"].shift()).cumsum()
    df.iloc[0, df.columns.get_loc("bout_id")] = 0  # type: ignore # First bout should be 0

    df["artefacts_bout"] = (series >= artefact_min_value) & (
        series <= artefact_max_value
    )
    df["artefacts_bout_id"] = (
        df["artefacts_bout"] != df["artefacts_bout"].shift()
    ).cumsum()
    df.iloc[0, df.columns.get_loc("artefacts_bout_id")] = 0  # type: ignore # First bout should be 0

    artefacts = (
        df[~df["artefacts_bout"]]
        .groupby("artefacts_bout_id")
        .apply(
            lambda x: _get_artefacts(
                x, artefact_max_duration, artefact_between_duration, df
            ),
            include_groups=False,
        )
    )
    artefacts = artefacts[artefacts].index
    df.loc[df["bout_id"].isin(artefacts), "bout"] = True
    df["bout_id"] = (df["bout"] != df["bout"].shift()).cumsum()
    df.iloc[0, df.columns.get_loc("bout_id")] = 0  # type: ignore # First bout should be 0

    bouts = (
        df[df["bout"]]
        .groupby("bout_id")
        .apply(lambda x: _get_bouts(x, bout_min_duration), include_groups=False)
    )
    bouts = bouts[bouts].index
    df["bout"] = False
    df.loc[df["bout_id"].isin(bouts), "bout"] = True

    bouts = df["bout"]
    return bouts
