#to be updated
import psycopg2
DATABASE_URL = "postgresql://app:password@postgres:5432/appdb"


def test_failure_recovery():
    conn = psycopg2.connect(DATABASE_URL)

