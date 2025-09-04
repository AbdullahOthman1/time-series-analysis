import argparse
import sys
import time
from datetime import datetime, timezone

import psutil

from database.insertion import get_db_conn, insert_job, insert_readings_batch

BATCH_SIZE = 60  # Insert each 60 seconds


def parse_duration(text: str) -> int:
    """
    Accepts:
      - pure seconds: "90"
      - with suffix: "90s", "2m", "1h"
      - combos: "1h30m", "2m15s", "1h2m3s"
    Returns total seconds (int).
    """
    text = text.strip().lower()
    if text.isdigit():
        return int(text)

    total = 0
    num = ""
    for ch in text:
        if ch.isdigit():
            num += ch
            continue
        if not num:
            raise ValueError(f"Invalid duration near '{ch}'")
        val = int(num)
        if ch == 'h':
            total += val * 3600
        elif ch == 'm':
            total += val * 60
        elif ch == 's':
            total += val
        else:
            raise ValueError(f"Unknown duration unit '{ch}'")
        num = ""

    if num:  # trailing number without unit => seconds
        total += int(num)
    if total <= 0:
        raise ValueError("Duration must be > 0 seconds")
    return total


def read_cpu_percent_one_sec() -> float:
    return float(psutil.cpu_percent(interval=1))


def read_ram_percent_one_sec() -> float:
    val = float(psutil.virtual_memory().percent)
    time.sleep(1)
    return val


def main():
    parser = argparse.ArgumentParser(
        description="Record CPU or RAM usage every second and store in Postgres."
    )
    parser.add_argument("duration", help='Total time (e.g., "100", "2m", "1h30m").')
    parser.add_argument(
        "metric",
        choices=["CPU", "RAM", "cpu", "ram"],
        help="Which metric to record.",
    )
    parser.add_argument("description", help="Job description text.")
    args = parser.parse_args()

    try:
        total_seconds = parse_duration(args.duration)
    except ValueError as e:
        print(f"[Args] {e}", file=sys.stderr)
        sys.exit(1)

    metric = args.metric.upper()
    read_func = read_cpu_percent_one_sec if metric == "CPU" else read_ram_percent_one_sec

    start_time = datetime.now(timezone.utc)

    conn = get_db_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                job_id = insert_job(cur, start_time, metric, args.description)
                print(f"[OK] Started job {job_id} at {start_time.isoformat()} for {metric}")

        batch = []
        collected = 0

        for _ in range(total_seconds):
            # reading timestamp is when we *took* the reading (not when stored)
            reading_time = datetime.now(timezone.utc)
            reading_val = read_func()

            batch.append((reading_time, reading_val, job_id))
            collected += 1

            # Every BATCH_SIZE readings, write to DB
            if len(batch) == BATCH_SIZE:
                with conn:
                    with conn.cursor() as cur:
                        insert_readings_batch(cur, batch)
                print(f"[DB] Inserted {len(batch)} readings (total so far: {collected})")
                batch.clear()

        # Insert any remaining readings after the loop
        if batch:
            with conn:
                with conn.cursor() as cur:
                    insert_readings_batch(cur, batch)
            print(f"[DB] Inserted final {len(batch)} readings (grand total: {collected})")

        print("[DONE] All readings recorded.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
