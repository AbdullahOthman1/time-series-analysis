from typing import Iterable, Tuple, Optional
import pandas as pd
from psycopg2.extras import execute_values

# Reuse your existing connection helper
from database.insertion import get_db_conn


def read_hardware_usage(job_id: str) -> pd.DataFrame:
    """
    Read hardware_usage data into a pandas DataFrame.
    Optionally filter by job_id.
    Returns columns: id, job_id, reading, date_time
    """
    conn = get_db_conn()
    try:
        sql = """
            SELECT id, job_id, reading, date_time
            FROM public."hardware_usage"
        """
        params = None
        if job_id:
            sql += " WHERE job_id = %s"
            params = (job_id,)

        df = pd.read_sql(sql, conn, params=params)

        if not df.empty:
            df["date_time"] = pd.to_datetime(df["date_time"], utc=True)
            df["reading"] = df["reading"].astype(float).round(4)

        return df
    finally:
        conn.close()


def write_rolling_values(rows: Iterable[Tuple]) -> int:
    """
    Bulk insert into the public.rolling_window table.

    rows: iterable of (date_time, rolling_value, job_id)
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
                    INSERT INTO public."rolling_window" (date_time, rolling_value, job_id)
                    VALUES %s
                    """,
                    rows,
                )
        return len(rows)
    finally:
        conn.close()
