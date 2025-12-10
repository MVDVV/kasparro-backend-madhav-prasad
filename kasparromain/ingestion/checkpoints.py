# ingestion/checkpoints.py
import os
import time
import csv
import json
import requests
from datetime import datetime
from core.db import get_db_conn, ensure_tables
from dotenv import load_dotenv

load_dotenv()

SOURCE_API_URL = os.getenv("SOURCE_API_URL", "https://jsonplaceholder.typicode.com/posts")
POLL_SECONDS = int(os.getenv("ETL_POLL_SECONDS", "10"))

def get_checkpoint(conn, source):
    cur = conn.cursor()
    cur.execute("SELECT last_offset, last_ts FROM checkpoints WHERE source = %s;", (source,))
    row = cur.fetchone()
    cur.close()
    if row:
        return row[0], row[1]
    return None, None

def set_checkpoint(conn, source, last_offset=None, last_ts=None):
    cur = conn.cursor()
    cur.execute("""
      INSERT INTO checkpoints (source, last_offset, last_ts, updated_at)
      VALUES (%s,%s,%s,now())
      ON CONFLICT (source) DO UPDATE SET last_offset = EXCLUDED.last_offset, last_ts = EXCLUDED.last_ts, updated_at = EXCLUDED.updated_at;
    """, (source, last_offset, last_ts))
    conn.commit()
    cur.close()