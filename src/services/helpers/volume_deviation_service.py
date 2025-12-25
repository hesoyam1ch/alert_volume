import datetime
from typing import List, Optional

from src.models.order_book_models import DeviationType, VolumeDeviation, OrderBookVolumes, OrderBookUsdt, \
    VolumeDeviationUsdt
from src.services.helpers.order_book_handler import OrderBookHandler


class VolumeDeviationDetector:
    def __init__(
            self,
            period_minutes: int = 60,
            threshold_persentage: float = 20.0
    ):
        self.period_minutes = period_minutes
        self.threshold_persentage = threshold_persentage



    def calculate_weighted_average(
            self,
            data: List,
            value_attr: str
    ) -> Optional[float]:
        if not data:
            return None

        now = datetime.datetime.now()
        weighted_sum = 0.0
        weight_sum = 0.0

        for record in data:
            value = getattr(record, value_attr)
            timestamp = datetime.datetime.fromtimestamp(record.timestamp)
            age_minutes = (now - timestamp).total_seconds() / 60

            half_life = self.period_minutes / 2
            weight = 2 ** (-age_minutes / half_life)

            weighted_sum += value * weight
            weight_sum += weight

        return weighted_sum / weight_sum if weight_sum > 0 else None

    def detect_limits_deviations(
            self,
            current_volumes: OrderBookUsdt,
            historical_data: List
    ) -> List[VolumeDeviationUsdt]:
        deviations = []

        if len(historical_data) < 5:
            return deviations

        historical_avarage_limit_volume_ask = OrderBookHandler.calculate_avarage_historical_volume(historical_data,is_ask=True)
        historical_avarage_limit_volume_bid = OrderBookHandler.calculate_avarage_historical_volume(historical_data)


        if historical_avarage_limit_volume_bid and historical_avarage_limit_volume_ask > 0:

            current_volume_bid_with_percentage = \
                historical_avarage_limit_volume_bid * (1 + self.threshold_persentage / 100)

            current_volume_ask_with_percentage = \
                historical_avarage_limit_volume_ask * (1 + self.threshold_persentage / 100)

            if current_volumes.avarage_ask_limit_volume > current_volume_ask_with_percentage:
                deviations.append(VolumeDeviationUsdt(
                    symbol=current_volumes.symbol,
                    timestamp=current_volumes.timestamp,
                    deviation_type=DeviationType.ASKS_HIGH,
                    current_value=current_volumes.avarage_ask_limit_volume,
                    threshold_percent=self.threshold_persentage
                ))

            if current_volumes.avarage_bid_limit_volume > current_volume_bid_with_percentage:
                deviations.append(VolumeDeviationUsdt(
                    symbol=current_volumes.symbol,
                    timestamp=current_volumes.timestamp,
                    deviation_type=DeviationType.BIDS_HIGH,
                    current_value=current_volumes.avarage_bid_limit_volume,
                    threshold_percent=self.threshold_persentage
                ))

        return deviations

    def detect_deviations(
            self,
            current_volumes: OrderBookVolumes,
            historical_data: List
    ) -> List[VolumeDeviation]:
        deviations = []

        if len(historical_data) < 5:
            return deviations


        avg_asks = self.calculate_weighted_average(
            historical_data,
            'volume_asks_upper'
        )

        if avg_asks and avg_asks > 0:
            asks_deviation_pct = (
                    (current_volumes.volume_asks_upper - avg_asks) / avg_asks * 100
            )

            if asks_deviation_pct > self.threshold_persentage:
                deviations.append(VolumeDeviation(
                    symbol=current_volumes.symbol,
                    timestamp=current_volumes.timestamp,
                    deviation_type=DeviationType.ASKS_HIGH,
                    current_value=current_volumes.volume_asks_upper,
                    weighted_avg=avg_asks,
                    deviation_percent=asks_deviation_pct,
                    threshold_percent=self.threshold_persentage
                ))

            elif asks_deviation_pct < self.threshold_persentage:
                deviations.append(VolumeDeviation(
                    symbol=current_volumes.symbol,
                    timestamp=current_volumes.timestamp,
                    deviation_type=DeviationType.ASKS_LOW,
                    current_value=current_volumes.volume_asks_upper,
                    weighted_avg=avg_asks,
                    deviation_percent=asks_deviation_pct,
                    threshold_percent=self.threshold_persentage
                ))

        avg_bids = self.calculate_weighted_average(
            historical_data,
            'volume_bids_lower'
        )

        if avg_bids and avg_bids > 0:
            bids_deviation_pct = (
                    (current_volumes.volume_bids_lower - avg_bids) / avg_bids * 100
            )

            if bids_deviation_pct > self.threshold_persentage:
                deviations.append(VolumeDeviation(
                    symbol=current_volumes.symbol,
                    timestamp=current_volumes.timestamp,
                    deviation_type=DeviationType.BIDS_HIGH,
                    current_value=current_volumes.volume_bids_lower,
                    weighted_avg=avg_bids,
                    deviation_percent=bids_deviation_pct,
                    threshold_percent=self.threshold_persentage
                ))

            elif bids_deviation_pct < self.threshold_persentage:
                deviations.append(VolumeDeviation(
                    symbol=current_volumes.symbol,
                    timestamp=current_volumes.timestamp,
                    deviation_type=DeviationType.BIDS_LOW,
                    current_value=current_volumes.volume_bids_lower,
                    weighted_avg=avg_bids,
                    deviation_percent=bids_deviation_pct,
                    threshold_percent=self.threshold_persentage
                ))

        return deviations