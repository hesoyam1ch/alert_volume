import datetime
from typing import List

from src.db.entities.order_book_vol_usdt import OrderBookVolumesHistoryUsdt
from src.models.order_book_models import OrderBookVolumes, OrderBookUsdt
from datetime import datetime


class OrderBookHandler:
    @staticmethod
    def calculate_mid_price(best_bid: float, best_ask: float) -> float:
        return (best_bid + best_ask) / 2

    @staticmethod
    def calculate_avarage_historical_volume(orders_list: list[OrderBookVolumesHistoryUsdt], is_ask=False) -> float:
        sum = 0.0
        for order in orders_list:
            if is_ask:
                sum += order.avarage_ask_volume
            else:
                sum += order.avarage_bids_volume

        avarage_limit_price = sum / len(orders_list)
        return avarage_limit_price


    @staticmethod
    def calculate_avarage_limit_price(orders_list: list) -> float:
        sum = 0.0
        for order in orders_list:
            sum += order

        avarage_limit_price = sum / len(orders_list)
        return avarage_limit_price

    @staticmethod
    def calculate_volume_to_price( orders: List[List[float]], target_price: float,is_ask: bool) -> float:
        total_volume = 0.0
        for price, volume in orders:
            if is_ask:
                if price <= target_price:
                    total_volume += volume
                else:
                    break
            else:
                if price >= target_price:
                    total_volume += volume
                else:
                    break
        return total_volume

    @classmethod
    def process_orderbook_second(cls, ob: dict) -> OrderBookUsdt:
        volumes_bid = []
        volumes_ask = []
        bid_array = ob['bids']
        ask_array = ob['asks']
        best_bid = ob['bids'][0][0]
        best_ask = ob['asks'][0][0]


        max_len = max(len(bid_array), len(ask_array))

        for i in range(max_len):
            if i < len(bid_array):
                bid = bid_array[i]
                bp, ba = bid[0], bid[1]
                volumes_bid.append(bp * ba)

            if i < len(ask_array):
                ask = ask_array[i]
                ap, aa = ask[0], ask[1]
                volumes_ask.append(ap * aa)

        mid_price = cls.calculate_mid_price(best_bid, best_ask)

        bid_avarage_order_is_usdt = cls.calculate_avarage_limit_price(volumes_bid)
        ask_avarage_order_is_usdt = cls.calculate_avarage_limit_price(volumes_ask)

        return OrderBookUsdt(
            symbol=ob['symbol'],
            timestamp=datetime.now(),
            mid_price=mid_price,
            avarage_ask_limit_volume = ask_avarage_order_is_usdt,
            avarage_bid_limit_volume = bid_avarage_order_is_usdt,
            upper_percent= 0,
            lower_percent = 0,
            best_bid=best_bid,
            best_ask=best_ask,
            nonce=ob['nonce']
        )



    @classmethod
    def process_orderbook(cls, ob: dict) -> OrderBookVolumes:
        best_bid = ob['bids'][0][0]
        best_ask = ob['asks'][0][0]

        mid_price = cls.calculate_mid_price(best_bid, best_ask)

        price_upper_level = mid_price * (1 + 0 / 100)
        price_lower_level = mid_price * (1 - 0 / 100)

        volume_asks = cls.calculate_volume_to_price(
            ob['asks'],
            price_upper_level,
            is_ask=True
        )

        volume_bids = cls.calculate_volume_to_price(
            ob['bids'],
            price_lower_level,
            is_ask=False
        )

        return OrderBookVolumes(
            symbol=ob['symbol'],
            timestamp=datetime.now(),
            mid_price=mid_price,
            price_upper_level=price_upper_level,
            price_lower_level=price_lower_level,
            volume_asks_upper=volume_asks,
            volume_bids_lower=volume_bids,
            upper_percent= 0,
            lower_percent = 0,
            best_bid=best_bid,
            best_ask=best_ask,
            nonce=ob['nonce']
        )


