from __future__ import annotations
import pandas as pd
from .base import MissingValueStrategy

class ForwardFill(MissingValueStrategy):
    """Notebook: fill_forward(df, col, limit=None)"""
    def __init__(self, col: str, limit: int | None = None):
        self.col = col
        self.limit = limit

    def fit(self, df: pd.DataFrame) -> "ForwardFill":
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out[self.col] = out[self.col].ffill(limit=self.limit)
        return out


class BackwardFill(MissingValueStrategy):
    """Notebook: fill_backward(df, col, limit=None)"""
    def __init__(self, col: str, limit: int | None = None):
        self.col = col
        self.limit = limit

    def fit(self, df: pd.DataFrame) -> "BackwardFill":
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out[self.col] = out[self.col].bfill(limit=self.limit)
        return out


class WindowMeanFill(MissingValueStrategy):
    """Notebook: fill_with_window_mean(df, col, window, min_periods=1, center=False)"""
    def __init__(self, col: str, window: int, min_periods: int = 1, center: bool = False):
        self.col = col
        self.window = window
        self.min_periods = min_periods
        self.center = center

    def fit(self, df: pd.DataFrame) -> "WindowMeanFill":
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        s = df[self.col]
        roll = s.rolling(window=self.window, min_periods=self.min_periods, center=self.center).mean()
        out = df.copy()
        out[self.col] = s.where(~s.isna(), roll)
        return out


class LinearInterpolationFill(MissingValueStrategy):
    """Notebook: fill_linear_interpolation(df, col, limit_direction='both', limit=None)"""
    def __init__(self, col: str, limit_direction: str = "both", limit: int | None = None):
        self.col = col
        self.limit_direction = limit_direction
        self.limit = limit

    def fit(self, df: pd.DataFrame) -> "LinearInterpolationFill":
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out[self.col] = df[self.col].interpolate(
            method="linear",
            limit_direction=self.limit_direction,
            limit=self.limit
        )
        return out
