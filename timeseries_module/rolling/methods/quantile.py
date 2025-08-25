import pandas as pd

def rolling_quantile(
    df: pd.DataFrame,
    value_column: str,
    window: int,
    q: float = 0.5,
    min_periods: int = 1,
    center: bool = False,
    method: str | None = None,
    output_column: str | None = None,
) -> pd.DataFrame:
    """
    Rolling quantile using the NEW pandas API (>= 2.2), which uses `method=...`
    instead of the deprecated/removed `interpolation=`.

    Parameters
    ----------
    q : float
        The quantile in [0, 1].
    method : str | None
        Quantile algorithm name per pandas >= 2.2 (e.g., "linear", etc.).
        If None, pandas' default is used (currently "linear").
    """
    out = df.copy()
    col = output_column or f"{value_column}_roll_q{q:g}"
    roll = out[value_column].rolling(window=window, min_periods=min_periods, center=center)

    if method is None:
        out[col] = roll.quantile(q)
    else:
        out[col] = roll.quantile(q, method=method)

    return out
