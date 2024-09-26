from datetime import timedelta

import pandas as pd


def gap_splitter(
    df: pd.DataFrame,
    min_duration: timedelta,
) -> pd.Series:
    splitted = df.index.diff() > min_duration  # type: ignore
    splitted = pd.Series(splitted, index=df.index)
    splitted = splitted.apply(lambda x: 1 if x else 0).cumsum() + 1

    return splitted.astype("UInt16")
