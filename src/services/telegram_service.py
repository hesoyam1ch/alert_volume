import aiohttp
import textwrap

from src.models.order_book_models import DeviationType, VolumeDeviation, VolumeDeviationUsdt


class TelegramService:

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/{self.bot_token}/sendMessage"

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

            <b>Current Value:</b> {deviation.current_value:.5f}
            
            <b>Time:</b> {deviation.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        """).strip()

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload) as response:
                    if response.status == 200:
                        return True
                    else:
                        error_text = await response.text()
                        print(f"❌ Telegram error {response.status}: {error_text}")
                        return False
        except Exception as e:
            print(f"❌ Failed to send Telegram message: {e}")
            return False

    # async def send_deviation_alert(self, deviation: VolumeDeviation):
    #
    #     emoji_map = {
    #         DeviationType.ASKS_HIGH: "🔴📈",
    #         DeviationType.ASKS_LOW: "🟢📉",
    #         DeviationType.BIDS_HIGH: "🟢📈",
    #         DeviationType.BIDS_LOW: "🔴📉"
    #     }
    #
    #     type_description = {
    #         DeviationType.ASKS_HIGH: "Increased ASKS volume (upper level)",
    #         DeviationType.ASKS_LOW: "Decreased ASKS volume (upper level)",
    #         DeviationType.BIDS_HIGH: "Increased BIDS volume (lower level)",
    #         DeviationType.BIDS_LOW: "Decreased BIDS volume (lower level)"
    #     }
    #
    #     emoji = emoji_map.get(deviation.deviation_type, "⚠️")
    #     desc = type_description.get(deviation.deviation_type, "DEVIATION")
    #
    #     message = textwrap.dedent(f"""
    #         {emoji} <b>VOLUME DEVIATION ALERT</b>
    #
    #         <b>Symbol:</b> {deviation.symbol}
    #         <b>Type:</b> {desc}
    #
    #         <b>Current Value:</b> {deviation.current_value:.5f}
    #         <b>Weighted Avg:</b> {deviation.weighted_avg:.5f}
    #         <b>Deviation:</b> {deviation.deviation_percent:+.2f}%
    #
    #         <b>Time:</b> {deviation.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
    #     """).strip()
    #
    #     payload = {
    #         "chat_id": self.chat_id,
    #         "text": message,
    #         "parse_mode": "HTML"
    #     }
    #
    #     try:
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(self.api_url, json=payload) as response:
    #                 if response.status == 200:
    #                     return True
    #                 else:
    #                     error_text = await response.text()
    #                     print(f"❌ Telegram error {response.status}: {error_text}")
    #                     return False
    #     except Exception as e:
    #         print(f"❌ Failed to send Telegram message: {e}")
    #         return False
