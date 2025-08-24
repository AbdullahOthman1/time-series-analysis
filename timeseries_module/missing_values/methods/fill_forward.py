import pandas as pd

def fill_forward(df: pd.DataFrame, value_column: str, limit: int = None) -> pd.DataFrame:
    """
    Fill missing values forward (previous valid observation is carried forward).
    """
    out = df.copy()
    out[value_column] = out[value_column].ffill(limit=limit)
    return out
