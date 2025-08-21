from __future__ import annotations
import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import LocalOutlierFactor

from .base import OutlierStrategy

# ---------------- Z-SCORE ----------------
class ZScoreOutliers(OutlierStrategy):
    """Drop rows where |z-score| > threshold for a single column."""
    def __init__(self, col: str, threshold: float = 3.0):
        self.col = col
        self.threshold = threshold

    def fit(self, df: pd.DataFrame) -> "ZScoreOutliers":
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        s = df[self.col]
        mu, sigma = s.mean(skipna=True), s.std(skipna=True, ddof=0)
        if sigma == 0 or np.isnan(sigma):
            return df.copy()
        z = (s - mu) / sigma
        return df.loc[z.abs() <= self.threshold].copy()


# ---------------- IQR ----------------
class IQROutliers(OutlierStrategy):
    """Drop rows outside [Q1 - k*IQR, Q3 + k*IQR] for a single column."""
    def __init__(self, col: str, k: float = 1.5):
        self.col = col
        self.k = k

    def fit(self, df: pd.DataFrame) -> "IQROutliers":
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        s = df[self.col]
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0 or np.isnan(iqr):
            return df.copy()
        lower, upper = q1 - self.k * iqr, q3 + self.k * iqr
        return df.loc[s.between(lower, upper, inclusive="both")].copy()


# ---------------- LINEAR REGRESSION (residual z-score) ----------------
class LinearRegressionOutliers(OutlierStrategy):
    """
    Fit linear regression y ~ time, drop rows with large residual z-scores.
    """
    def __init__(self, value_col: str, time_col: str, z_thresh: float = 3.0):
        self.value_col = value_col
        self.time_col = time_col
        self.z_thresh = z_thresh

    def fit(self, df: pd.DataFrame) -> "LinearRegressionOutliers":
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        time = pd.Series(df[self.time_col]).rank(method="first").to_numpy().reshape(-1, 1)
        values = df[self.value_col]
        mask = ~values.isna()

        if mask.sum() < 2:
            return df.copy()

        model = LinearRegression().fit(time[mask], values[mask])
        preds = model.predict(time[mask])
        residuals = values[mask] - preds

        mu, sigma = residuals.mean(), residuals.std(ddof=0)
        if sigma == 0 or np.isnan(sigma):
            return df.copy()

        z = (residuals - mu) / sigma
        keep_mask = pd.Series(True, index=df.index)
        keep_mask.loc[df.index[mask]] = np.abs(z) <= self.z_thresh
        return df.loc[keep_mask].copy()


# ---------------- LOCAL OUTLIER FACTOR ----------------
class LOFOutliers(OutlierStrategy):
    """
    Drop rows flagged as outliers by Local Outlier Factor (LOF).
    If include_time=True, use [time, y] as features.
    """
    def __init__(self, y_col: str, time_col: str | None = None,
                 n_neighbors: int = 20, contamination: float = 0.05,
                 include_time: bool = False):
        self.y_col = y_col
        self.time_col = time_col
        self.n_neighbors = n_neighbors
        self.contamination = contamination
        self.include_time = include_time

    def fit(self, df: pd.DataFrame) -> "LOFOutliers":
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        yvals = pd.to_numeric(df[self.y_col], errors="coerce")
        valid_mask = yvals.notna()

        if self.include_time and self.time_col is not None:
            tx = df[self.time_col]
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

        lof = LocalOutlierFactor(n_neighbors=self.n_neighbors, contamination=self.contamination)
        labels = lof.fit_predict(X)  # 1=inlier, -1=outlier

        keep_mask = pd.Series(True, index=df.index)
        keep_mask.loc[valid_mask.index[valid_mask]] = (labels == 1)
        return df.loc[keep_mask].copy()
