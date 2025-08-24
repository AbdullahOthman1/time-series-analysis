import pandas as pd

def window_mean(df: pd.DataFrame, value_column: str, window: int = 3, min_periods: int = 1, center: bool = False) -> pd.DataFrame:
    """
    Fill missing values using rolling window mean.
    """
    s = df[value_column]
    roll = s.rolling(window=window, min_periods=min_periods, center=center).mean()
    out = df.copy()
    out[value_column] = s.where(~s.isna(), roll)
    return out
