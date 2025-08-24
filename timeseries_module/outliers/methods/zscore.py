import numpy as np
import pandas as pd

def remove_outliers_zscore(df: pd.DataFrame, value_column: str, threshold: float = 3.0) -> pd.DataFrame:
    """
    Remove rows where the z-score of `value_column` exceeds `threshold`.
    Keeps NaN rows.
    """
    s = df[value_column]
    mu = s.mean(skipna=True)
    sigma = s.std(skipna=True, ddof=0)

    if sigma == 0 or np.isnan(sigma):
        return df.copy()

    z = (s - mu) / sigma
    mask = s.isna() | (z.abs() <= threshold)
    return df.loc[mask].copy()
