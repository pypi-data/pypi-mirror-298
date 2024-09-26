import pandas as pd


def mode(x: pd.Series):
    # TODO: Could be not mode but that 2/3 or 75% of data are the same, otherwise mixed
    # FIXME: This is real problem, because mode is not always the best solution. Should be discussed. One idea is to ffill or bfill after downsampled.
    m = x.mode()

    if m.empty:
        return None
    # elif len(m) > 1:
    #     raise ValueError("Multiple modes found.")
    #     # return None
    else:
        return m[0]


def sum(x: pd.Series):
    return x.sum(min_count=1)
