import pandas as pd

def apply_rolling(func, df: pd.DataFrame, value_column: str, **kwargs) -> pd.DataFrame:
    """
    Apply a rolling function to a DataFrame column.
    """
    return func(df, value_column=value_column, **kwargs)



def compute_rolling(
    df: pd.DataFrame,
    rolling_fn,            
    value_column: str,
    **kwargs
) -> pd.DataFrame:
    """
    Wrapper that applies a rolling function with simple defaults.

    df: pd.DataFrame
        The input data.
    rolling_fn: function
        One of your rolling methods:
          - rolling_mean / rolling_median / rolling_sum / rolling_min / rolling_max
          - rolling_std / rolling_var
          - rolling_quantile
    value_column: str
        Column to operate on.
    kwargs:
        Extra parameters to override the defaults (window, min_periods, center, ddof, q, method, output_column, ...).
    """
    if value_column not in df.columns:
        raise ValueError(f"value_column '{value_column}' not found in DataFrame.")

    name = getattr(rolling_fn, "__name__", "").lower()
    options = {}

    # Common defaults
    options["min_periods"] = 1
    options["center"] = False

    # Window defaults (you can change these if you prefer)
    if "std" in name or "var" in name:
        options["window"] = 14
        options["ddof"] = 0
    else:
        options["window"] = 7

    # Quantile defaults
    if "quantile" in name:
        options["q"] = 0.5
        options["method"] = "linear"

    options.update(kwargs)

    if int(options.get("window", 0)) <= 0:
        raise ValueError("Please provide a positive 'window' (e.g., window=7).")
    if "quantile" in name:
        q = float(options.get("q", 0.5))
        if not (0.0 <= q <= 1.0):
            raise ValueError("'q' must be in [0, 1].")

    return apply_rolling(rolling_fn, df, value_column, **options)

