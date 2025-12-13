from ingestion.unify_schema import upsert_normalized
from datetime import datetime
from core.db import get_db_conn, release_db_conn
import os
DATABASE_URL = os.getenv
def test_incremental_upsert():
    conn = get_db_conn()

    canonical_id = "eth100"
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
    release_db_conn(conn)

    assert count == 1, "Incremental ingestion should not create duplicates"
