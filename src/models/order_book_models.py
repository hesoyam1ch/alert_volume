from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass
class OrderBookVolumes:
    symbol: str
    timestamp: datetime
    mid_price: float
    price_upper_level: float
    price_lower_level: float
    volume_asks_upper: float
    volume_bids_lower: float
    upper_percent: float
    lower_percent: float
    best_bid: float
    best_ask: float
    nonce: int


@dataclass
class OrderBookUsdt:
    symbol: str
    timestamp: datetime
    mid_price: float
    avarage_ask_limit_volume: float
    avarage_bid_limit_volume: float
    upper_percent: float
    lower_percent: float
    best_bid: float
    best_ask: float
    nonce: int

class DeviationType(Enum):
    ASKS_HIGH = "asks_high"
    ASKS_LOW = "asks_low"
    BIDS_HIGH = "bids_high"
    BIDS_LOW = "bids_low"


@dataclass
class VolumeDeviation:
    symbol: str
    timestamp: datetime
    deviation_type: DeviationType
    current_value: float
    weighted_avg: float
    deviation_percent: float
    threshold_percent: float

@dataclass
class VolumeDeviationUsdt:
    symbol: str
    timestamp: datetime
    deviation_type: DeviationType
    current_value: float
    threshold_percent: float



