from typing import Iterable, Tuple
import pandas as pd

# DB helpers
from database.rolling_io import read_hardware_usage, write_rolling_values

from timeseries_module.rolling.interface import compute_rolling
from timeseries_module.rolling.methods import rolling_mean


def extract_rolling_column(df_with_roll: pd.DataFrame,value_column:str, window_name: str) -> pd.Series:
    """
    Extract and normalize the rolling column created by the module.
    Column is expected to be named: f"{value_column}_roll_{window_name}"
    """
    col = f"{value_column}_roll_{window_name}"
    if col not in df_with_roll.columns:
        raise ValueError(
            f"Expected column '{col}' not found. "
            f"Make sure your module outputs this exact column."
        )
    # normalize precision for DB (NUMERIC(7,4))
    return df_with_roll[col].astype(float).round(4)


def to_rolling_rows(df: pd.DataFrame, rolling_col: pd.Series) -> Iterable[Tuple]:
    """
    Convert DataFrame to rows for insertion into rolling_window:
      (date_time, rolling_value, job_id)
    """
    for dt, val, jid in zip(df["date_time"], rolling_col, df["job_id"]):
        yield (
            dt.to_pydatetime() if isinstance(dt, pd.Timestamp) else dt,
            None if pd.isna(val) else float(val),
            str(jid),
        )


def process_rolling_windows(window_name: str, value_column:str, job_id:str) -> int:
    """
    Full pipeline:
      1) Read hardware_usage (optionally filtered by job_id)
      2) Apply rolling module -> adds 'roll_window_{window_name}'
      3) Extract that column as rolling_value
      4) Write (date_time, rolling_value, job_id) to public.rolling_window

    Returns number of rows written.
    """
    # 1) Read
    df_raw = read_hardware_usage(job_id=job_id)
    if df_raw.empty:
        print("[INFO] No hardware_usage data found for the given scope.")
        return 0

    # 2) Apply rolling
    df_roll = compute_rolling(df_raw, rolling_fn=rolling_mean, value_column="reading", window=10)

    # 3) Extract rolling values and shape rows
    rolling_col = extract_rolling_column(df_roll, window_name=window_name, value_column=value_column)

    # Optional sanity checks
    if len(df_roll) != len(df_raw):
        raise AssertionError("Rolling module changed the row count; it should keep the same rows.")

    rows = list(to_rolling_rows(df_roll, rolling_col))

    # 4) Persist
    inserted = write_rolling_values(rows)
    print(f"[INFO] Wrote {inserted} rows into public.rolling_window for window '{window_name}'.")
    return inserted


if __name__ == "__main__":
    process_rolling_windows(window_name="mean",value_column="reading", job_id="fd31539a-8c69-4886-bfef-909714854c8d")
