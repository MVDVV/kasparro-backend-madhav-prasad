# api/main.py
import os
import time
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from core.db import get_db_conn, release_db_conn, ensure_tables
from schemas.api_responses import DataResponse, DataRow
from schemas.api_responses import HealthResponse, ETLStatus




app = FastAPI(title= "Backend & ETL - Assignment, API")

# ensure tables exist on startup
@app.on_event("startup")
def startup():
    time.sleep(5)  # wait for the DB to be ready
    ensure_tables()




@app.get("/health", response_model=HealthResponse)
def health():
    db_ok = False
    etl_status = None

    try:
        conn = get_db_conn()
        cur = conn.cursor()

        # --- Check DB connectivity ---
        cur.execute("SELECT 1;")
        db_ok = True

        # --- Get ETL last run ---
        cur.execute("""
            SELECT source, success, finished_at, started_at
            FROM etl_runs
            ORDER BY finished_at DESC
            LIMIT 1;
        """)
        row = cur.fetchone()

        if row:
            etl_status = ETLStatus(
                source=row[0],
                success=row[1],
                finished_at=row[2],
                started_at=row[3]
            )

        cur.close()

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    
    release_db_conn(conn) # release the connection back to the pool
    return HealthResponse(
        status="ok" if db_ok else "error",
        timestamp=datetime.utcnow(),
        db_connected=db_ok,
        etl_last_run=etl_status
    )



@app.get("/data", response_model=DataResponse)
def get_data(

    #pagination and filtering input parameters

    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    source: Optional[str] = None,       # coingecko, csv, etc.
    from_ts: Optional[datetime] = None, # start timestamp
    to_ts: Optional[datetime] = None,   # end timestamp
):
    start_time = time.perf_counter()
    conn = get_db_conn()
    cur = conn.cursor()
    where = []
    params = []
    if source:
        where.append("source = %s")
        params.append(source)
    if from_ts:
        where.append("ts >= %s")
        params.append(from_ts)
    if to_ts:
        where.append("ts <= %s")
        params.append(to_ts)

    #command construction
    where_clause = ("WHERE " + " AND ".join(where)) if where else ""
    count_q = f"SELECT count(*) FROM normalized {where_clause};"
    cur.execute(count_q, tuple(params))


    result = cur.fetchone()
    total = result[0] if result else 0      #THIS LINE IS BECAUSE FETCHONE CAN RETURN NONE
    offset = (page - 1) * page_size # calculate offset for the page
    q = f"""
        SELECT id, canonical_id, name, value, ts, source
        FROM normalized
        {where_clause}
        ORDER BY ts DESC NULLS LAST
        LIMIT %s OFFSET %s;
    """
    cur.execute(q, tuple(params) + (page_size, offset))
    rows = cur.fetchall()
    cur.close()
    release_db_conn(conn) # release the connection back to the pool
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000  
    return DataResponse(
        request_id=os.urandom(8).hex(),
        page=page,
        page_size=page_size,
        total=total,
        api_latency_ms=latency_ms,
        results=[
            DataRow(
                id=str(r[0]),
                canonical_id=r[1],
                name=r[2],
                value=r[3],
                ts=r[4],
                source=r[5]
            )
            for r in rows
        ] # type: ignore ,pyright is tweaking
    )



@app.get("/stats")
def stats():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
      SELECT source, COUNT(*) as cnt
      FROM normalized
      GROUP BY source;
    """)
    rows = cur.fetchall()
    cur.close()
    release_db_conn(conn) # release the connection back to the pool
    return {"by_source": {r[0]: r[1] for r in rows}}
