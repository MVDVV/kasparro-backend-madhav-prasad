from ingestion.unify_schema import upsert_normalized
from ingestion.api_source import insert_raw_api
from datetime import datetime
from core.db import get_db_conn, release_db_conn    
import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")
def test_etl_transformation_basic():
    # Setup test DB connection
    conn = get_db_conn()

    # Fake raw payload (as returned from API)
    fake_coin = {
        "id": "bitcoin",
        "name": "Bitcoin",
        "current_price": 42000,
    }

    raw_id = insert_raw_api(conn, "bitcoin", fake_coin)

    # ETL: insert into normalized
    upsert_normalized(
        conn=conn,
        canonical_id="bitcoin123test",
        name="Bitcoin123test",
        value=42000,
        ts=datetime.utcnow(),
        last_updated=datetime.utcnow(),
        source="coingecko",
        raw_ref=raw_id,
    )

    cur = conn.cursor()
    cur.execute("SELECT name, value FROM normalized WHERE canonical_id='bitcoin123test'")
    row = cur.fetchone()
    cur.close()
    release_db_conn(conn)

    assert row[0] == "Bitcoin123test" #type: ignore
    assert row[1] == 42000.   #type: ignore
