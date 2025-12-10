#testing incremental ingestions
from ingestion.unify_schema import upsert_normalized
from datetime import datetime
import psycopg2
DATABASE_URL = "postgresql://app:password@postgres:5432/appdb"
def test_incremental_upsert():
    conn = psycopg2.connect(DATABASE_URL)

    canonical_id = "coingecko:eth:100"
    # Define a UUID constant for the test

    upsert_normalized(
        conn, canonical_id, "Ethereum", 2000, datetime.utcnow(),datetime.utcnow(), "coingecko" #skip the raw_uuid field (FORIGN KEY)
    )
    upsert_normalized(  # run again
        conn, canonical_id, "Ethereum", 2100,datetime.utcnow(),datetime.utcnow(), "coingecko" #skip the raw_uuid field (FORIGN KEY)
    )

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM normalized WHERE canonical_id=%s", (canonical_id,))
    count = cur.fetchone()[0] #type: ignore
    cur.close()

    assert count == 1, "Incremental ingestion should not create duplicates"
