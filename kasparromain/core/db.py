# core/db.py
import os
import psycopg2
import psycopg2.pool
from pathlib import Path
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DATABASE_URL_LOCAL") or "postgresql://app:password@postgres:5432/appdb"

connection_pool =  psycopg2.pool.SimpleConnectionPool(minconn = 4 ,maxconn = 4, dsn = DATABASE_URL)

def get_db_conn():
    conn = connection_pool.getconn() 
    return conn

def release_db_conn(conn):
    connection_pool.putconn(conn)

def ensure_tables():
    # If you prefer to run init_db.sql from compose, this is optional.
    BASE_DIR = Path(__file__).resolve().parents[0]
    SQL_FILE = BASE_DIR / "init_db.sql"
    SQL = SQL_FILE.read_text()
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(SQL)
    conn.commit()
    cur.close()
    release_db_conn(conn) # release the connection back to the pool
