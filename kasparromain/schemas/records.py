# Pydantics schema for unified records
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CoinGeckoItem(BaseModel):
    id: str                     #"bitcoin"
    symbol: Optional[str]       #"btc"
    name: Optional[str]         #"Bitcoin"

    current_price: Optional[float]
    market_cap: Optional[float]
    total_volume: Optional[float]
    price_change_percentage_1h_in_currency: Optional[float]
    last_updated : Optional[datetime]
    raw_payload: dict           #raw JSON
    ts: datetime = Field(default_factory=datetime.utcnow)

    @property
    def canonical_id(self) -> str:

        """Unique row key based on source + coin id + timestamp."""

        return f"coingecko:{self.id}:{int(self.ts.timestamp())}"

    @property
    def normalized_value(self) -> float:

        """Primary numeric field for normalized table."""
        return float(self.current_price or 0.0)

    @property
    def display_name(self) -> str:

        return self.name or self.id or "unknown"