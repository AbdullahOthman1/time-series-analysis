import pandas as pd

def linear_interpolation(df: pd.DataFrame, value_column: str, limit_direction: str = "both", limit: int = None) -> pd.DataFrame:
    """
    Fill missing values using linear interpolation.
    """
    out = df.copy()
    out[value_column] = df[value_column].interpolate(method="linear", limit_direction=limit_direction, limit=limit)
    return out
