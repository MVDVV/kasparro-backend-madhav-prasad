# ingestion/csv_source.py
import json
import os
import csv
from ingestion.checkpoints import set_checkpoint, get_checkpoint
from ingestion.unify_schema import upsert_normalized
from datetime import datetime
from core.db import get_db_conn, ensure_tables 
from dotenv import load_dotenv

load_dotenv()

SOURCE_CSV_PATH = os.getenv("SOURCE_CSV_PATH", "/app/data/sample_source.csv")

# raw CSV insert 
def insert_raw_csv(conn, line_no, payload):
    cur = conn.cursor()
    cur.execute("INSERT INTO raw_csv (line_no, payload) VALUES (%s,%s) RETURNING id;", (line_no, json.dumps(payload)))
    raw_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return raw_id

# main CSV ingestion function
def process_csv(conn):
    """Read CSV, process new lines using checkpoint as last processed line number."""
    last_offset, _ = get_checkpoint(conn, "csv")
    try:
        last_line = int(last_offset) if last_offset else 0
    except:
        last_line = 0

    processed = 0
    if not os.path.exists(SOURCE_CSV_PATH):
        print("CSV not found at", SOURCE_CSV_PATH)
        return 0

    with open(SOURCE_CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=1):
            if idx <= last_line:
                continue
            raw_id = insert_raw_csv(conn, idx, row)
            canonical_id = f"csv:{idx}"
            name = row.get("name") or row.get("title") or "csv-row"
            try:
                value = float(row.get("value") or len(name))
            except:
                value = float(len(name))
            ts = datetime.utcnow()
            upsert_normalized(conn, canonical_id, name, value, ts,last_updated=ts, source="csv", raw_ref=raw_id)
            processed += 1
            last_line = idx

    if processed:
        set_checkpoint(conn, "csv", last_offset=str(last_line), last_ts=datetime.utcnow())
    return processed