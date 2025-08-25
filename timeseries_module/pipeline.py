from pathlib import Path
import pandas as pd
from .outliers.interface import handle_outliers
from .missing_values.interface import apply_missing_values
from .rolling.interface import compute_rolling

def run_pipeline(
    input_df: pd.DataFrame,
    output_path: str | Path,
    outlier_sensitivity_degree: str,
    value_column: str,
    missing_value_function=None,  
    outlier_fn=None,             
    time_column: str | None = None,
    rolling_fn=None,          
    rolling_kwargs: dict | None = None,
    export: bool = True,
) -> pd.DataFrame:
    """
    Run a minimal cleaning pipeline on a time-series DataFrame, with an optional rolling step.

    This pipeline:
    1) Optionally fills missing values in a single target column.
    2) Optionally removes outliers from that column using a sensitivity profile
        ('low' | 'medium' | 'high') defined in the outliers interface.
    3) Optionally applies a rolling function to the cleaned `value_column`.
    4) Optionally saves outputs to disk:
        - If step (1) or (2) ran, writes <output_path>/clean.csv.
        - If step (3) ran (i.e., a rolling function was provided), writes <output_path>/rolling.csv.

    Parameters
    ----------
    input_df : pd.DataFrame
        Input data. The function works on a copy and never mutates this object.
    output_path : str | pathlib.Path
        Directory where CSV files will be written if `export=True`.
    outlier_sensitivity_degree : str
        One of {'low', 'medium', 'high'}. Controls how aggressive outlier removal is.
        (Mapped to method-specific settings inside `handle_outliers`.)
    value_column : str
        Name of the numeric column to process (for both missing values and outliers).
    missing_value_function : callable or None, optional
        A function like `fill_forward`, `fill_backward`, `window_mean`, or
        `linear_interpolation`. It will be called as:
            missing_value_function(df, value_column)
        If None, the missing-values step is skipped.
    outlier_fn : callable or None, optional
        A function like `remove_outliers_zscore`, `remove_outliers_iqr`,
        `remove_outliers_linear_regression`, or `remove_outliers_lof`.
        It is applied via `handle_outliers(...)`. If None, the outliers step is skipped.
    time_column : str or None, optional
        Optional time column used by certain outlier methods (e.g., linear regression,
        optionally LOF). Ignored by methods that don't need it.
    rolling_fn : callable or None, optional
        Optional rolling function (e.g., `rolling_mean`, `rolling_median`, `rolling_std`,
        `rolling_var`, `rolling_sum`, `rolling_min`, `rolling_max`, `rolling_quantile`).
        If provided, it is applied AFTER missing-values and outliers on `value_column`.
    rolling_kwargs : dict or None, optional
        Extra parameters for `rolling_fn` (e.g., {"window": 7} or {"window": 21, "q": 0.5, "method": "linear"}).
    export : bool, optional
        If True (default), writes `<output_path>/clean.csv` when missing-values or outliers are applied,
        and writes `<output_path>/rolling.csv` when a rolling function is applied.

    Returns
    -------
    pd.DataFrame
        The cleaned DataFrame after running the selected steps (i.e., after missing-values/outliers).
    """

    df = input_df.copy()

    # 1) Missing values (skip if None)
    if missing_value_function is not None:
        df = apply_missing_values(missing_value_function, df, value_column)

    # 2) Outliers (skip if None)
    if outlier_fn is not None:
        df = handle_outliers(
            df,
            outlier_fn,
            value_column=value_column,
            sensitivity_degree=outlier_sensitivity_degree,
            time_column=time_column,
        )

    # 3) Rolling (optional; run on the cleaned df)
    rolling_df = None
    if rolling_fn is not None:
        rolling_df = compute_rolling(
            df=df,
            rolling_fn=rolling_fn,
            value_column=value_column,
            **(rolling_kwargs or {})
        )

    # 4) Export final result
    if export:
        out_dir = Path(output_path)
        out_dir.mkdir(parents=True, exist_ok=True)

        if missing_value_function is not None or outlier_fn is not None:
            df.to_csv(out_dir / "clean.csv", index=False)

        if rolling_fn is not None and rolling_df is not None:
            rolling_df.to_csv(out_dir / "rolling.csv", index=False)

    return df
