#to be updated
import psycopg2
import os
from core.db import get_db_conn, release_db_conn
DATABASE_URL = os.getenv("DATABASE_URL")


def test_failure_recovery():
    conn = get_db_conn()
    release_db_conn(conn)

