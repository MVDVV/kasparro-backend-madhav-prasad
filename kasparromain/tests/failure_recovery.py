#this needs rewriting
import psycopg2
DATABASE_URL = "postgresql://app:password@postgres:5432/appdb"


def test_failure_recovery():
    conn = psycopg2.connect(DATABASE_URL)

    # simulate a crash: incomplete checkpoint
    cur = conn.cursor()
    cur.execute("UPDATE checkpoints SET last_offset='BROKEN_STATE'")
    conn.commit()
    cur.close()

    # run ETL again — should not crash
    processed = -1
    processed = run_etl_once()
    assert processed != -1