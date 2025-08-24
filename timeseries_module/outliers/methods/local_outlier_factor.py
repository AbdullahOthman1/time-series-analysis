import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from pandas.api.types import is_datetime64_any_dtype
from sklearn.neighbors import LocalOutlierFactor

def remove_outliers_lof(
    df: pd.DataFrame,
    value_column: str,
    time_column: str = None,
    n_neighbors: int = 20,
    contamination: float = 0.05,
    include_time: bool = False,
) -> pd.DataFrame:
    """
    Use Local Outlier Factor (LOF) to remove outliers in `value_column`.
    Optionally include time as a feature.
    """
    yvals = pd.to_numeric(df[value_column], errors="coerce")
    valid_mask = yvals.notna()

    if include_time and time_column is not None:
        tx = df[time_column]
        if is_datetime64_any_dtype(tx):
            tnum = mdates.date2num(pd.to_datetime(tx))
        else:
            tnum = pd.to_numeric(tx, errors="coerce").to_numpy()

        valid_mask = valid_mask & pd.notna(tnum)
        X = np.column_stack([tnum[valid_mask], yvals[valid_mask].to_numpy()])
    else:
        X = yvals[valid_mask].to_numpy().reshape(-1, 1)

    if X.shape[0] == 0:
        return df.copy()

    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
    labels = lof.fit_predict(X)

    inlier_mask = pd.Series(True, index=df.index)
    inlier_mask.loc[valid_mask.index[valid_mask]] = (labels == 1)

    return df.loc[inlier_mask].copy()
