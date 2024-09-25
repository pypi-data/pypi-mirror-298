from dataclasses import dataclass

from emp_orderly_types import PerpetualAssetType


@dataclass
class Order:
    price: float
    quantity: float


@dataclass
class OrderBook:
    timestamp: int
    asks: list[Order]
    bids: list[Order]


@dataclass
class BidAsk:
    bid: Order
    ask: Order


class OrderlyOrderBook:
    account_id: str
    pvt_hex: str

    def get_order_book(
        self, asset: PerpetualAssetType = PerpetualAssetType.BTC, limit=10
    ):
        response_json = self._send_request(f"v1/orderbook/{asset.value}")
        data = response_json["data"]
        timestamp = data["timestamp"]
        asks = []
        for ask in data["asks"][:limit]:
            asks.append(Order(price=ask["price"], quantity=ask["quantity"]))
        bids = []
        for bid in data["bids"][:limit]:
            bids.append(Order(price=bid["price"], quantity=bid["quantity"]))

        return OrderBook(
            timestamp,
            asks,
            bids,
        )

    def get_order_book_at_index(
        self, asset: PerpetualAssetType = PerpetualAssetType.BTC, index=0
    ):
        order_book = self.get_order_book(asset)
        return BidAsk(
            order_book.bids[index],
            order_book.asks[index],
        )

    def _send_request(self, path, body=None, params=None, method="GET"):
        raise NotImplementedError()
