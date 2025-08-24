import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def remove_outliers_linear_regression(
    df: pd.DataFrame,
    value_column: str,
    time_column: str = None,
    threshold: float = 3.0,
) -> pd.DataFrame:
    """
    Fit a linear regression of value vs. time,
    then remove rows whose residual z-score exceeds `threshold`.
    Rows with NaN in `value_column` are kept.
    """
    # Use row order if no time column
    if time_column is None:
        time = pd.Series(np.arange(len(df)), index=df.index)
    else:
        time = df[time_column]

    time_rank = pd.Series(time).rank(method="first").to_numpy().reshape(-1, 1)
    values = df[value_column]

    fit_mask = ~values.isna()
    if fit_mask.sum() < 2:
        return df.copy()

    model = LinearRegression().fit(time_rank[fit_mask], values[fit_mask])
    preds = model.predict(time_rank[fit_mask])

    residuals = values[fit_mask] - preds
    sigma = residuals.std(ddof=0)

    if sigma == 0 or np.isnan(sigma):
        return df.copy()

    z = (residuals - residuals.mean()) / sigma

    keep_idx = df.index[fit_mask][np.abs(z) <= threshold].tolist()
    keep_idx += df.index[~fit_mask].tolist()

    return df.loc[keep_idx].copy()
