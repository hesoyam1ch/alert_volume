from src.services.helpers.order_book_service import OrderBookService
from src.services.helpers.volume_deviation_service import VolumeDeviationDetector


class UserProcessor:
    def __init__(
        self,
        detector: VolumeDeviationDetector,
        order_book_service: OrderBookService,
        alert_service,
        period_minutes: int,
    ):
        self.detector = detector
        self.order_book_service = order_book_service
        self.alert_service = alert_service
        self.period_minutes = period_minutes

    async def on_volumes(self, volumes):
        print(f"[DEBUG] UserProcessor tick for {volumes.symbol}")
        history = await self.order_book_service.get_usdt_limits_for_period(
            volumes.symbol,
            self.period_minutes
        )

        deviations = self.detector.detect_limits_deviations(volumes, history)

        for d in deviations:
            await self.alert_service.send_deviation_alert(d)
