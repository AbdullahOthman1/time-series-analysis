# timeseries_module/pipeline.py
from pathlib import Path
import pandas as pd
from .outliers.interface import handle_outliers
from .missing_values.interface import apply_missing_values

def run_pipeline(
    input_df: pd.DataFrame,
    output_path: str | Path,
    outlier_sensitivity_degree: str,
    value_column: str,
    missing_value_function=None,  
    outlier_fn=None,             
    time_column: str | None = None,
    export: bool = True,
) -> pd.DataFrame:
    """
    Run a minimal, two-step cleaning pipeline on a time-series DataFrame.

    This pipeline:
      1) Optionally fills missing values in a single target column.
      2) Optionally removes outliers from that column using a sensitivity profile
        ('low' | 'medium' | 'high') defined in the outliers interface.
      3) Optionally saves the final result to <output_path>/clean.csv.

    Parameters
    ----------
    input_df : pd.DataFrame
        Input data. The function works on a copy and never mutates this object.
    output_path : str | pathlib.Path
        Directory where the final CSV will be written if `export=True`.
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
    export : bool, optional
        If True (default), writes the final DataFrame to `<output_path>/clean.csv`.

    Returns
    -------
    pd.DataFrame
        The cleaned DataFrame after running the selected steps.

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

    # 3) Export final result
    if export:
        out_dir = Path(output_path)
        out_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_dir / "clean.csv", index=False)

    return df
