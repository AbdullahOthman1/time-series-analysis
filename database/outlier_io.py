from typing import Iterable, Tuple, Optional
import pandas as pd
from psycopg2.extras import execute_values

from .insertion import get_db_conn


def read_hardware_usage(job_id: Optional[str] = None) -> pd.DataFrame:
    conn = get_db_conn()
    try:
        base_sql = """
            SELECT id, job_id, reading, date_time
            FROM public."hardware_usage"
        """
        params = None
        if job_id:
            base_sql += " WHERE job_id = %s"
            params = (job_id,)

        df = pd.read_sql(base_sql, conn, params=params)

        # Normalize types (safeguards)
        if not df.empty:
            # Ensure date_time is tz-aware pandas Timestamp
            df["date_time"] = pd.to_datetime(df["date_time"], utc=True)
            # Keep numeric precision consistent with DB scale (7,4)
            df["reading"] = df["reading"].astype(float).round(4)

        return df

    finally:
        conn.close()


def write_outlier_flags(rows: Iterable[Tuple]) -> int:
    """
    Bulk insert into the public.outlier table.
    rows: iterable of (date_time, reading, outlier_flag, job_id)

    Returns number of rows inserted.
    """
    rows = list(rows)
    if not rows:
        return 0

    conn = get_db_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                execute_values(
                    cur,
                    """
                    INSERT INTO public."outlier" (date_time, reading, outlier_flag, job_id)
                    VALUES %s
                    """,
                    rows,
                )
        return len(rows)
    finally:
        conn.close()
