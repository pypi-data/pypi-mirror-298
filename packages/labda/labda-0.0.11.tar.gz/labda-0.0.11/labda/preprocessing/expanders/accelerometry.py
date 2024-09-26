import numpy as np
import pandas as pd

from ...structure.validation import Column
from ..utils.common import columns_checker


def get_vector_magnitude(
    df: pd.DataFrame,
    cols: list[Column | str],
) -> pd.Series:
    columns_checker(df, cols, True)  # type: ignore

    vm = np.linalg.norm(
        df[cols].astype(float),
        axis=1,
    )
    return pd.Series(vm, index=df.index)
