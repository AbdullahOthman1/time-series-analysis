from typing import Iterable, Tuple
import pandas as pd

from database.outlier_io import read_hardware_usage, write_outlier_flags
from timeseries_module.outliers.interface import handle_outliers
from timeseries_module.outliers.methods.zscore import remove_outliers_zscore


def build_outlier_flags(df_raw: pd.DataFrame, df_kept: pd.DataFrame) -> pd.DataFrame:
    if df_raw.empty:
        return df_raw.assign(outlier_flag=pd.Series(dtype=bool))

    df_flagged = df_raw.copy()
    df_flagged["outlier_flag"] = True

    if "id" not in df_kept.columns:
        raise ValueError("df_kept must include the original 'id' column for matching.")

    kept_ids = set(df_kept["id"].tolist())
    df_flagged.loc[df_flagged["id"].isin(kept_ids), "outlier_flag"] = False

    df_flagged["reading"] = df_flagged["reading"].astype(float).round(4)
    df_flagged["date_time"] = pd.to_datetime(df_flagged["date_time"], utc=True)

    return df_flagged


def to_outlier_rows(df_flagged: pd.DataFrame) -> Iterable[Tuple]:
    """
    Convert flagged DataFrame to an iterable of tuples in the order:
      (date_time, reading, outlier_flag, job_id)
    """
    for row in df_flagged.itertuples(index=False):
        yield (
            row.date_time.to_pydatetime() if isinstance(row.date_time, pd.Timestamp) else row.date_time,
            float(row.reading),
            bool(row.outlier_flag),
            str(row.job_id),
        )


def process_outliers(job_id:str) -> int:
    """
    Full pipeline:
      1) Read hardware_usage (filtered by job_id)
      2) Apply outlier removal -> df_kept (non-outliers)
      3) Merge to create outlier_flag for all original rows
      4) Write results into public.outlier

    Returns number of rows written.
    """
    # 1) Read
    df_raw = read_hardware_usage(job_id=job_id)
    if df_raw.empty:
        print("[INFO] No hardware_usage data found for the given scope.")
        return 0

    # 2) Outlier removal
    df_kept = handle_outliers(df=df_raw, outlier_fn=remove_outliers_zscore,sensitivity_degree="HIGH",value_column="reading",time_column="date_time")

    # 3) Build flags
    df_flagged = build_outlier_flags(df_raw, df_kept)

    # 4) Persist
    rows = list(to_outlier_rows(df_flagged))
    inserted = write_outlier_flags(rows)

    print(f"[INFO] Wrote {inserted} rows into public.outlier "
          f"(kept={len(df_kept)}, outliers={len(df_raw) - len(df_kept)}).")
    return inserted


if __name__ == "__main__":
    process_outliers(job_id="fd31539a-8c69-4886-bfef-909714854c8d")
