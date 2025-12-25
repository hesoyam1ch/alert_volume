import textwrap

from aiogram import Bot

from src.models.order_book_models import VolumeDeviation, VolumeDeviationUsdt, DeviationType


class UserAlertService:
    def __init__(self, bot: Bot, user_id: int):
        self.bot = bot
        self.user_id = user_id

    async def send_text(self, text: str):
        await self.bot.send_message(
            chat_id=self.user_id,
            text=text,
            parse_mode="HTML",
        )

    async def send_deviation_alert(self, deviation: VolumeDeviationUsdt):
        emoji_map = {
            DeviationType.ASKS_HIGH: "🔴📈",
            DeviationType.ASKS_LOW: "🟢📉",
            DeviationType.BIDS_HIGH: "🟢📈",
            DeviationType.BIDS_LOW: "🔴📉"
        }

        type_description = {
            DeviationType.ASKS_HIGH: "Increased ASKS volume (upper level)",
            DeviationType.ASKS_LOW: "Decreased ASKS volume (upper level)",
            DeviationType.BIDS_HIGH: "Increased BIDS volume (lower level)",
            DeviationType.BIDS_LOW: "Decreased BIDS volume (lower level)"
        }

        emoji = emoji_map.get(deviation.deviation_type, "⚠️")
        desc = type_description.get(deviation.deviation_type, "DEVIATION")

        message = textwrap.dedent(f"""
            {emoji} <b>VOLUME DEVIATION ALERT</b>

            <b>Symbol:</b> {deviation.symbol}
            <b>Type:</b> {desc}

            <b>Current Value:</b> {deviation.current_value:.2f} USDT
            <b>Threshold:</b> {deviation.threshold_percent:.2f}%
            <b>Time:</b> {deviation.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        """).strip()

        try:
            await self.bot.send_message(
                chat_id=self.user_id,
                text=message,
                parse_mode="HTML"
            )
            return True
        except Exception as e:
            print(f"❌ Failed to send Telegram message: {e}")
            return False