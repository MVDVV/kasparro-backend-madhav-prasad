from ingestion.unify_schema import upsert_normalized
from ingestion.api_source import insert_raw_api
from datetime import datetime
import psycopg2

DATABASE_URL = "postgresql://app:password@postgres:5432/appdb"
def test_etl_transformation_basic():
    # Setup test DB connection
    conn = psycopg2.connect(DATABASE_URL)

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
        canonical_id="coingecko:bitcoin:123",
        name="Bitcoin",
        value=42000,
        ts=datetime.utcnow(),
        last_updated=datetime.utcnow(),
        source="coingecko",
        raw_ref=raw_id,
    )

    cur = conn.cursor()
    cur.execute("SELECT name, value FROM normalized WHERE canonical_id='coingecko:bitcoin:123'")
    row = cur.fetchone()
    cur.close()

    assert row[0] == "Bitcoin" #type: ignore
    assert row[1] == 42000.   #type: ignore