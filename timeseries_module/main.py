from pathlib import Path
import pandas as pd
from .pipeline import run_pipeline

def main(
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
    Main entry point for the time series module.

     What it does (on `value_column`):
      1) (optional) Fill missing values using the function you pass (e.g., fill_forward).
      2) (optional) Remove outliers using a sensitivity profile: 'low' | 'medium' | 'high'.
      3) (optional) Apply a rolling function (e.g., rolling_mean/median/std/var/sum/min/max/quantile).
      4) (optional) Save outputs: <output_path>/clean.csv (cleaned), and if a rolling function was applied,
        <output_path>/rolling.csv.

    Parameters
    ----------
    input_df : pd.DataFrame
        Input DataFrame (not modified in place).
    output_path : str | pathlib.Path
        Directory to write the final CSV if `export=True`.
    outlier_sensitivity_degree : {'low','medium','high'}
        Controls outlier aggressiveness (mapped inside `handle_outliers`).
    value_column : str
        Name of the numeric column to process.
    missing_value_function : callable or None, optional
        e.g., fill_forward, fill_backward, window_mean, linear_interpolation.
        Called as: missing_value_function(df, value_column). Use None to skip.
    outlier_fn : callable or None, optional
        e.g., remove_outliers_zscore, remove_outliers_iqr,
        remove_outliers_linear_regression, remove_outliers_lof. Use None to skip.
    time_column : str or None, optional
        Optional time column used by some outlier methods.
    rolling_fn : callable or None, optional
        Optional rolling function applied after missing/outliers (e.g., rolling_mean, rolling_quantile).
        If provided and `export=True`, a separate `rolling.csv` is written.
    rolling_kwargs : dict or None, optional
        Extra parameters for `rolling_fn` (e.g., {"window": 7} or {"window": 21, "q": 0.5, "method": "linear"}).
    export : bool, optional
        If True (default), writes `<output_path>/clean.csv` and, when `rolling_fn` is provided,
        `<output_path>/rolling.csv`.

    Returns
    -------
    pd.DataFrame
        The cleaned DataFrame.
    """
    return run_pipeline(
        input_df=input_df,
        output_path=output_path,
        outlier_sensitivity_degree=outlier_sensitivity_degree,
        value_column=value_column,
        missing_value_function=missing_value_function,
        outlier_fn=outlier_fn,
        time_column=time_column,
        rolling_fn=rolling_fn,
        rolling_kwargs=rolling_kwargs,
        export=export,
    )
