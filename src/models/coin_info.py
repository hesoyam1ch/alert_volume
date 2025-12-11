import dataclasses

from dataclasses import dataclass
from datetime import datetime

@dataclass
class CoinInfo:
    symbol : str
    ask_volume_positive : float
    bid_volume_negative : float
    calculate_percentage : float
    upper_price : float
    average_price : float
    lower_price : float
    average_volume :float
    timestamp : datetime

