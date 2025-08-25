import pandas as pd

def rolling_var(
    df: pd.DataFrame,
    value_column: str,
    window: int,
    min_periods: int = 1,
    center: bool = False,
    ddof: int = 0,
    output_column: str | None = None,
) -> pd.DataFrame:
    
    out = df.copy()
    col = output_column or f"{value_column}_roll_var"
    out[col] = out[value_column].rolling(window=window, min_periods=min_periods, center=center).var(ddof=ddof)
    return out
