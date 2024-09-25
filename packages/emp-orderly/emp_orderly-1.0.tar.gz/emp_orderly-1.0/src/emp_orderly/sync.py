from decimal import Decimal
from typing import ClassVar, Optional

from pydantic import BaseModel, PrivateAttr
import requests
from requests import Request, Session

from emp_orderly_types import (
    MarketInfo,
    Order,
    OrderResponse,
    OrderType,
    PerpetualAssetType,
    Position,
    PositionData,
)
from .history import OrderlyHistory
from .order_book import OrderlyOrderBook
from .utils import OrderlySigner


class EmpyrealOrderlySyncSDK(BaseModel, OrderlyOrderBook, OrderlyHistory):
    BASE_URL: ClassVar[str] = "https://api-evm.orderly.org"

    account_id: str
    pvt_hex: str
    _signer: OrderlySigner = PrivateAttr()

    def model_post_init(self, __context) -> None:
        self._signer = OrderlySigner(self.account_id, self.pvt_hex)

    def asset_history(self):
        response_json = self._send_request("v1/asset/history", method="GET")
        return response_json

    def get_market_info(self, asset: PerpetualAssetType) -> MarketInfo:
        response = requests.get(
            f"{self.BASE_URL}/v1/public/futures/{asset.value}",
        )
        response_json = response.json()
        if not response_json["success"]:
            raise ValueError(f"Invalid Response: {response_json}")
        return MarketInfo(**response_json["data"])

    def orderly_key(self):
        return self._signer.orderly_key()

    def get_account(self, address, broker_id="empyreal"):
        response = requests.get(
            f"{self.BASE_URL}/v1/get_account",
            params={"address": address, "broker_id": broker_id},
        )
        if response.status_code != 200:
            raise ValueError(response.text)
        response_json = response.json()
        if not response_json["success"]:
            raise ValueError(response_json)
        return response.json()["data"]

    def get_orderly_key(self, account_id, orderly_key):
        """Check the validity of an Orderly access key attached to the account."""

        response = requests.get(
            f"{self.BASE_URL}/v1/get_orderly_key",
            params={"account_id": account_id, "orderly_key": orderly_key},
        )
        if response.status_code != 200:
            raise ValueError(response.text)
        response_json = response.json()
        if not response_json["success"]:
            raise ValueError(response_json)
        return response.json()["data"]

    def get_info(self):
        response_json = self._send_request("v1/client/info")
        return response_json["data"]

    def holdings(self):
        response_json = self._send_request("v1/client/holding")
        return response_json["data"]["holding"]

    def positions(self) -> PositionData:
        response_json = self._send_request("v1/positions")
        return PositionData(**response_json["data"])

    def position(self, asset: PerpetualAssetType) -> Optional[Position]:
        positions = self.positions().rows
        filtered_positions = [
            position for position in positions if position.symbol == asset
        ]
        if len(filtered_positions) == 0:
            return None
        return filtered_positions[0]

    def close_position(self, asset: PerpetualAssetType) -> OrderResponse | None:
        positions = self.positions().rows
        filtered_positions = [
            position for position in positions if position.symbol == asset
        ]
        if len(filtered_positions) == 0:
            return None
        position = filtered_positions[0]
        if position.position_qty == 0:
            return None
        is_buy = position.position_qty < 0
        return self.make_order(
            abs(position.position_qty),
            asset=asset,
            is_buy=is_buy,
            reduce_only=True,
        )

    def make_limit_order(
        self,
        amount,
        price: float | Decimal,
        asset: PerpetualAssetType = PerpetualAssetType.BTC,
        is_buy=True,
        reduce_only: bool = False,
    ) -> OrderResponse:
        body = dict(
            order_quantity=float(amount),
            order_price=str(price),
            order_type=OrderType.LIMIT,
            side="BUY" if is_buy else "SELL",
            symbol=asset.value,
            reduce_only=reduce_only,
            order_tag="EMPYREAL",
        )
        response_json = self._send_request("v1/order", body=body, method="POST")
        if response_json["success"]:
            return OrderResponse(**response_json["data"])
        raise ValueError(response_json)

    def make_order(
        self,
        amount: Decimal,
        asset: PerpetualAssetType = PerpetualAssetType.BTC,
        is_buy=True,
        reduce_only: bool = False,
    ):
        body = dict(
            order_quantity=str(amount),
            order_type=OrderType.MARKET,
            side="BUY" if is_buy else "SELL",
            symbol=asset.value,
            reduce_only=reduce_only,
            order_tag="EMPYREAL",
        )

        response_json = self._send_request("v1/order", body=body, method="POST")
        if response_json["success"]:
            return OrderResponse(**response_json["data"])
        raise ValueError(response_json)

    def _orders(
        self,
        page: int = 1,
        size: int = 100,
        max_pages: int = 3,
        status: str | None = None,
        asset: Optional[PerpetualAssetType] = None,
    ):
        if max_pages == 0:
            return []
        response_json = self._send_request(
            "v1/orders/",
            params={
                "page": page,
                "size": size,
                "source": asset and asset.value,
                "status": status,
            },
        )

        # 'meta': {'total': 1, 'records_per_page': 25, 'current_page': 1}}
        meta = response_json["data"]["meta"]
        rows = response_json["data"]["rows"]
        if meta["total"] > 25:
            rows += self._orders(page=meta["current_page"] + 1, max_pages=max_pages - 1)
        return rows

    def close_orders(
        self,
        asset: PerpetualAssetType,
    ):
        reponse_json = self._send_request(
            "v1/orders",
            params={
                "symbol": asset.value,
            },
            method="DELETE",
        )
        return reponse_json

    def orders(
        self,
        size: int = 100,
        page: int = 1,
        max_pages: int = 3,
        status: str | None = None,
        asset: Optional[PerpetualAssetType] = None,
    ) -> list[Order]:
        # TODO: filter by asset type
        orders = self._orders(
            page=page, size=size, max_pages=max_pages, status=status, asset=asset
        )
        return [Order(**r) for r in orders]

    def _send_request(self, path, body=None, params=None, method="GET"):
        session = Session()
        res = session.send(
            self._signer.sign_request(
                Request(
                    method,
                    f"{self.BASE_URL}/{path}",
                    params=params,
                    json=body,
                ),
            )
        )
        if res.status_code != 200:
            print(res.status_code, res.text)
            # raise HTTPException(res.status_code, res.text)
            raise ValueError(400, "orderly error")
        response_json = res.json()
        if "success" in response_json:
            if not response_json["success"]:
                raise ValueError(response_json)
        if "s" in response_json:
            if not response_json["s"] == "ok":
                raise ValueError(response_json)
        return response_json

    def get_order_by_id(
        self,
        order_id: int,
    ):
        response_json = self._send_request(f"v1/order/{order_id}")
        return Order(**response_json["data"])
