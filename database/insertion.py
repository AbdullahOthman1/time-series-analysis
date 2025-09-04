import os
import sys
from typing import Iterable, Tuple
from datetime import datetime

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values

load_dotenv()

__all__ = [
    "get_db_conn",
    "insert_job",
    "insert_readings_batch",
]

def get_db_conn():
    try:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
    except Exception as e:
        print(f"[DB] Connection failed: {e}", file=sys.stderr)
        sys.exit(2)


def insert_job(cur, start_time_utc: datetime, resource: str, description: str) -> str:
    """
    Insert a new job row and return its ID.
    Assumes 'resource' matches ENUM resource_type ('CPU','RAM').
    """
    cur.execute(
        """
        INSERT INTO public."job" (start_time, resource, description)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (start_time_utc, resource, description),
    )
    return cur.fetchone()[0]


def insert_readings_batch(
    cur,
    rows: Iterable[Tuple[datetime, float, str]]
):
    """
    Bulk insert hardware readings.

    rows: iterable of (date_time, reading, job_id)
    """
    rows = list(rows)
    if not rows:
        return
    execute_values(
        cur,
        """
        INSERT INTO public."hardware_usage" (date_time, reading, job_id)
        VALUES %s
        """,
        rows,
    )
