# ingestion/api_source.py
import os
import time
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

from core.db import get_db_conn
from ingestion.unify_schema import upsert_normalized
from ingestion.checkpoints import set_checkpoint
from schemas.records import CoinGeckoItem

load_dotenv()

# parameters and fields for the CoinGecko API request

SOURCE_API_URL = os.getenv("SOURCE_API_URL", "https://api.coingecko.com/api/v3/coins/markets")
VS_CURRENCY = os.getenv("VS_CURRENCY", "usd")
CATEGORY = os.getenv("CATEGORY", "layer-1")
PRICE_CHANGE_PERCENTAGE = os.getenv("PRICE_CHANGE_PERCENTAGE", "1h")
INCLUDE_TOKENS = os.getenv("INCLUDE_TOKENS", "top")
SOURCE_NAME = os.getenv("SOURCE_NAME", "coingecko")
headers = {"x-cg-demo-api-key": os.getenv("API_KEY")}

#for insertion of raw api data
def insert_raw_api(conn, source_id, payload):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO raw_api (source_id, payload) VALUES (%s,%s) RETURNING id;",
        (source_id, json.dumps(payload)),
    )
    raw_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return raw_id

# Main ingestion function
def fetch_api(conn):
    """Fetches coin market data from CoinGecko every call (call frequency controlled by worker using POLL field"""
    try:
        params = {
            "vs_currency": VS_CURRENCY,
            "category": CATEGORY,
            "price_change_percentage": PRICE_CHANGE_PERCENTAGE,
            "include_tokens": INCLUDE_TOKENS,
        }

        response = requests.get(SOURCE_API_URL, params=params, headers=headers, timeout=15) # 
        response.raise_for_status()

        coins = response.json()
        processed = 0

        for coin in coins:
            try:
                cg = CoinGeckoItem(
                    id=coin.get("id"),
                    symbol=coin.get("symbol"),
                    name=coin.get("name"),
                    current_price=coin.get("current_price"),
                    market_cap=coin.get("market_cap"),
                    total_volume=coin.get("total_volume"),
                    price_change_percentage_1h_in_currency=coin.get("price_change_percentage_1h_in_currency"),
                    last_updated=coin.get("last_updated"),
                    raw_payload=coin
                )
            except Exception as e:
                print("Validation failed:", e)
                continue

            raw_id = insert_raw_api(conn, cg.id, cg.raw_payload)
            print("RAW INSERT SUCCEEDED",cg.id)

            upsert_normalized(
                conn=conn,
                canonical_id=cg.canonical_id,
                name=cg.display_name,
                value=cg.normalized_value,
                ts=cg.ts,
                last_updated=cg.last_updated,
                source=SOURCE_NAME,
                raw_ref=raw_id,
            )

            processed += 1

        if processed:
            set_checkpoint( # updating checkpoint after processing batch
                conn,
                "api",
                last_offset=str(datetime.utcnow()),
                last_ts=datetime.utcnow(),
            )

        return processed

    except Exception as e:
        print("Error insertion of coin from coins line:", e)
        return 0