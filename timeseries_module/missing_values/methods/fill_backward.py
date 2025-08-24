import pandas as pd

def fill_backward(df: pd.DataFrame, value_column: str, limit: int = None) -> pd.DataFrame:
    """
    Fill missing values backward (next valid observation is carried backward).
    """
    out = df.copy()
    out[value_column] = out[value_column].bfill(limit=limit)
    return out
