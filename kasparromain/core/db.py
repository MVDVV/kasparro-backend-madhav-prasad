# core/db.py
import os
import psycopg2
from pathlib import Path
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DATABASE_URL_LOCAL") or "postgresql://app:password@postgres:5432/appdb"

_conn = None

def get_db_conn():
    global _conn
    if _conn is None or _conn.closed:
        _conn = psycopg2.connect(DATABASE_URL)
    return _conn

def ensure_tables():
    BASE_DIR = Path(__file__).resolve().parents[0]
    SQL_FILE = BASE_DIR / "init_db.sql"
    SQL = SQL_FILE.read_text()
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(SQL)
    conn.commit()
    cur.close()
