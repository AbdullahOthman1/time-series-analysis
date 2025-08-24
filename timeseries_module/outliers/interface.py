import pandas as pd

_SENSITIVITY = {
    "low":    {"z_threshold": 4.0, "iqr_k": 3.0,  "lof": {"contamination": 0.01, "n_neighbors": 35}},
    "medium": {"z_threshold": 3.0, "iqr_k": 1.5,  "lof": {"contamination": 0.1, "n_neighbors": 20}},
    "high":   {"z_threshold": 2.0, "iqr_k": 1.0,  "lof": {"contamination": 0.20, "n_neighbors": 10}},
}

def apply_outliers(func, df: pd.DataFrame, value_column: str, **kwargs) -> pd.DataFrame:
    """
    Apply an outlier-removal function to a DataFrame column.

    func: function
        A function like:
            - remove_outliers_zscore
            - remove_outliers_iqr
            - remove_outliers_linear_regression
            - remove_outliers_lof
    df: pd.DataFrame
        The input DataFrame.
    value_column: str
        The column to apply the method on.
    kwargs:
        Extra parameters for the function:
            - threshold (e.g., threshold, n_neighbors, contamination, etc.).
    """
    return func(df, value_column, **kwargs)

def handle_outliers(df: pd.DataFrame, outlier_fn, value_column: str, sensitivity_degree, time_column: str = None, **kwargs) -> pd.DataFrame:
    """
    Wrapper that applies an outlier function using a hard-coded sensitivity level.

    df: pd.DataFrame
        The input data.
    outlier_fn: function
        A function like:
            - remove_outliers_zscore
            - remove_outliers_iqr
            - remove_outliers_linear_regression
            - remove_outliers_lof
    sensitivity_degree: str
        One of: 'low', 'medium', 'high'.
    value_column: str
        Name of the column to operate on.
    time_column: str or None
        Optional time column (used by linear_regression, optionally by LOF).
    kwargs:
        Extra parameters to override the defaults from sensitivity mapping.
    """

    if value_column not in df.columns:
        raise ValueError(f"value_column '{value_column}' not found in DataFrame.")
    if time_column is not None and time_column not in df.columns:
        raise ValueError(f"time_column '{time_column}' not found in DataFrame.")
    
    s = str(sensitivity_degree).lower()
    cfg = _SENSITIVITY.get(s, _SENSITIVITY["medium"])
    name = getattr(outlier_fn, "__name__", "")

    options = {}

    if "zscore" in name or "linear_regression" in name:
        options["threshold"] = cfg["z_threshold"]
        if "linear_regression" in name and time_column is not None:
            options["time_column"] = time_column

    elif "iqr" in name:
        options["threshold"] = cfg["iqr_k"]

    elif "lof" in name:
        options.update(cfg["lof"])
        if time_column is not None:
            options["time_column"] = time_column
            options.setdefault("include_time", True)

    options.update(kwargs)

    return apply_outliers(outlier_fn, df, value_column, **options)
