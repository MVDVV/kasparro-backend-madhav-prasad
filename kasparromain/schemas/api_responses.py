#response model here is used to define the structure of the response that the endpoint will return
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DataRow(BaseModel):
    id: str
    canonical_id: Optional[str]
    name: Optional[str]
    value: Optional[float]
    ts: Optional[datetime]
    source: Optional[str]


class DataResponse(BaseModel):
    request_id: str
    page: int
    page_size: int
    total: int
    api_latency_ms: float
    results: list[DataRow]

class ETLStatus(BaseModel):
    source: str
    success: bool
    finished_at: datetime
    started_at: Optional[datetime]


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    db_connected: bool
    etl_last_run: Optional[ETLStatus]