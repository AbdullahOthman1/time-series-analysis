import numpy as np
import pandas as pd

def remove_outliers_iqr(df: pd.DataFrame, value_column: str, threshold: float = 1.5) -> pd.DataFrame:
    """
    Remove rows outside [Q1 - threshold*IQR, Q3 + threshold*IQR] for `value_column`.
    Keeps NaN rows.
    """
    s = df[value_column]
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1

    if iqr == 0 or np.isnan(iqr):
        return df.copy()

    lower, upper = q1 - threshold * iqr, q3 + threshold * iqr
    mask = s.isna() | s.between(lower, upper)
    return df.loc[mask].copy()
