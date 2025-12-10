#common function for upserting into normalized table for API and CSV sources

def upsert_normalized(conn, canonical_id, name, value, ts, last_updated, source, raw_ref=None):
    cur = conn.cursor()
    cur.execute("""
      INSERT INTO normalized (canonical_id, name, value, ts, last_updated, source, raw_ref)
      VALUES (%s,%s,%s,%s,%s,%s,%s)
      ON CONFLICT (canonical_id, source) DO UPDATE
      SET name = EXCLUDED.name, value = EXCLUDED.value, ts = EXCLUDED.ts,last_updated = EXCLUDED.last_updated, raw_ref = EXCLUDED.raw_ref;
    """, (canonical_id, name, value, ts, last_updated, source, raw_ref))
    conn.commit()
    cur.close()