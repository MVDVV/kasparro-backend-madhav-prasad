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
    
class PaprikaItem(BaseModel):
    id: str                     #"btc-bitcoin"
    symbol: Optional[str]       #"btc"
    name: Optional[str]         #"Bitcoin"

    price_usd: Optional[float]
    market_cap_usd: Optional[float]
    volume_24h_usd: Optional[float]
    percent_change_1h: Optional[float]
    last_updated : Optional[datetime]
    raw_payload: dict           #raw JSON
    ts: datetime = Field(default_factory=datetime.utcnow)

    @property
    def canonical_id(self) -> str:

        """Unique row key based on source + coin id + timestamp."""

        return f"paprika:{self.id}:{int(self.ts.timestamp())}"

    @property
    def normalized_value(self) -> float:

        """Primary numeric field for normalized table."""
        return float(self.price_usd or 0.0)

    @property
    def display_name(self) -> str:

        return self.name or self.id or "unknown"
