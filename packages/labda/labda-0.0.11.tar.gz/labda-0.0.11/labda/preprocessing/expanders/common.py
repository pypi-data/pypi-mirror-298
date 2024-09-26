import pandas as pd

from ...structure.validation import Column


def get_timedelta(
    df: pd.DataFrame,
    name: Column = Column.TIMEDELTA,
) -> pd.Series:
    return pd.Series(df.index.diff(), index=df.index, name=name)  # type: ignore
