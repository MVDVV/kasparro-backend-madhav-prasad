# ingestion/worker.py
import os
import time
import csv
import json
from datetime import datetime
from core.db import get_db_conn, release_db_conn, ensure_tables
from dotenv import load_dotenv
from ingestion.api_source import fetch_api
from ingestion.csv_source import process_csv

load_dotenv()

POLL_SECONDS = int(os.getenv("ETL_POLL_SECONDS", "30"))

def main_loop():
    ensure_tables()
    conn = get_db_conn()
    print("Worker started, connecting to DB...")
    while True:
        start = datetime.utcnow()
        try:
            api_count = fetch_api(conn)
            api_count += fetch_api(conn,api_type="paprika")
            csv_count = process_csv(conn)
            # insert etl_run log
            if(api_count != 0):
                cur = conn.cursor()
                cur.execute("INSERT INTO etl_runs (source, started_at, finished_at, records_processed, success) VALUES (%s, %s, now(), %s, true);",("api",start,api_count))
                conn.commit()
                cur.close()
            if(csv_count != 0):
                cur = conn.cursor()
                cur.execute("INSERT INTO etl_runs (source, started_at, finished_at, records_processed, success) VALUES (%s, %s, now(), %s, true);",("csv",start,csv_count))
                conn.commit()
                cur.close()
        except KeyboardInterrupt:
            print("Worker shutting down...")
            break
        except Exception as e:
            print("Worker error:", e)
        time.sleep(POLL_SECONDS)
    
    release_db_conn(conn)


if __name__ == "__main__":
    main_loop()
