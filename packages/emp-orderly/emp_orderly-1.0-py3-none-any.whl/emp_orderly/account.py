from datetime import datetime
from decimal import Decimal
import time
from typing import ClassVar, Literal, Optional

from eth_rpc import PrivateKeyWallet
from eth_typing import HexAddress
import httpx
from pydantic import BaseModel, Field, PrivateAttr, model_validator
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
from .utils import OrderlySigner, from_address, orderly_register

CACHE_MARKET_INFO: dict[PerpetualAssetType, tuple[int, MarketInfo]] = {}


class EmpyrealOrderlySDK(BaseModel, OrderlyOrderBook, OrderlyHistory):
    """
    The Main Account Class for interacting with Orderly.

    Args:
        pvt_hex: This is the private key to be used for the signer
        account_id: The account you are executing transactions for.  By default,
                                    this will be the account id associated with the pvt_key.
        is_testnet: Whether to send requests to the testnet or production endpoint
    """

    def __init__(self, pvt_hex: str, account_id: str | None = None, is_testnet: bool = True):
        super().__init__(pvt_hex=pvt_hex, account_id=account_id or "", is_testnet=is_testnet)

    _BASE_URL: str = PrivateAttr()
    BASE_MAINNET_URL: ClassVar[str] = "https://api-evm.orderly.org"
    BASE_TESTNET_URL: ClassVar[str] = "https://testnet-api-evm.orderly.org"

    pvt_hex: str
    account_id: str = Field(default="")
    is_testnet: bool = Field(default=True)

    _signer: OrderlySigner = PrivateAttr()
    _wallet: PrivateKeyWallet = PrivateAttr()

    @model_validator(mode="after")
    def set_default_orderly_id(self):
        if self.account_id == "":
            self.account_id = from_address(self._wallet.address)
        return self

    def model_post_init(self, __context):
        self._signer = OrderlySigner(self.account_id, self.pvt_hex)
        self._wallet = PrivateKeyWallet(private_key=self.pvt_hex)
        if self.is_testnet:
            self._BASE_URL = self.BASE_TESTNET_URL
        else:
            self._BASE_URL = self.BASE_MAINNET_URL

    @classmethod
    async def register(cls, private_hex: str, chain_id: int = 42161, broker_id: str = "empyreal"):
        account_id = await orderly_register(private_hex, chain_id, broker_id)
        return cls(
            account_id=account_id,
            pvt_hex=private_hex,
        )

    async def asset_history(self):
        response_json = await self._send_request_async("v1/asset/history", method="GET")
        return response_json

    async def asset_info(self, asset: PerpetualAssetType):
        """This is useful for getting filter requirements"""
        response_json = await self._send_request_async(
            f"v1/public/info/{asset.value}", method="GET"
        )
        return response_json

    async def get_market_info(
        self,
        asset: PerpetualAssetType, ttl: int = 15,
    ) -> MarketInfo:
        """
        The `get_market_info` function retrieves market information for a specified asset, utilizing a cache
        to store and retrieve data efficiently.

        Args:
            asset: The `asset` parameter in the `get_market_info` function is of type `PerpetualAssetType`, which is used to specify the
                type of asset for which market information is being retrieved.
            ttl (int): The `ttl` parameter in the `get_market_info` function stands for "time to live"
                and it represents the maximum age in seconds that a cached market info for a
                specific asset is considered valid before it needs to be refreshed by making a new API request.
                Defaults to 15.

        Returns:
            This contains information about a specific asset in the market. If the information for the asset is already
                cached and within the specified time-to-live (TTL), the cached result is returned. Otherwise, a new request
                is made to fetch the market information from the API, and the retrieved data is stored in the cache before
                being returned
        """

        global CACHE_MARKET_INFO
        age, res = CACHE_MARKET_INFO.get(asset, (0, None))
        if (time.time() - age) < ttl and res is not None:
            return res
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._BASE_URL}/v1/public/futures/{asset.value}",
                timeout=20,
            )
        response_json = response.json()
        if not response_json["success"]:
            raise ValueError(f"Invalid Response: {response_json}")
        market_info = MarketInfo(**response_json["data"])
        CACHE_MARKET_INFO[asset] = (int(time.time()), market_info)
        return market_info

    def orderly_key(self):
        """Returns the orderly key for a user's account"""
        return self._signer.orderly_key()

    async def get_account(self, address: HexAddress, broker_id: str):
        """
        Check whether a wallet has a registered account with provided broker_id.

        https://orderly.network/docs/build-on-evm/evm-api/restful-api/public/check-if-wallet-is-registered
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._BASE_URL}/v1/get_account",
                params={"address": address, "broker_id": broker_id},
            )
        if response.status_code != 200:
            raise ValueError(response.text)
        response_json = response.json()
        if not response_json["success"]:
            raise ValueError(response_json)
        return response.json()["data"]

    async def get_orderly_key(self, account_id: str, orderly_key: str) -> dict[str, str]:
        """
        Check the validity of an Orderly access key attached to the account.

        Args:
            account_id: Your orderly account ID
            orderly_key: Your orderly key

        Returns:
            response_json: Your orderly key with scope, expiration and tag.
        """

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._BASE_URL}/v1/get_orderly_key",
                params={"account_id": account_id, "orderly_key": orderly_key},
                timeout=20,
            )
        if response.status_code != 200:
            raise ValueError(response.text)
        response_json = response.json()
        if not response_json["success"]:
            raise ValueError(response_json)
        return response.json()["data"]

    async def get_info(self):
        response_json = await self._send_request_async("v1/client/info")
        return response_json["data"]

    async def holdings(self):
        response_json = await self._send_request_async("v1/client/holding")
        return response_json["data"]["holding"]

    async def positions(self) -> PositionData:
        response_json = await self._send_request_async("v1/positions")
        return PositionData(**response_json["data"])

    async def position(self, asset: PerpetualAssetType) -> Optional[Position]:
        positions = (await self.positions()).rows
        filtered_positions = [
            position for position in positions if position.symbol == asset
        ]
        if len(filtered_positions) == 0:
            return None
        return filtered_positions[0]

    async def close_position(self, asset: PerpetualAssetType) -> OrderResponse | None:
        """Close all positions for a specific asset

        Args:
            asset: The `asset` to close
        Returns:
            If there are no positions to close it will return None, otherwise
                it returns an `OrderResponse`
        """
        positions = (await self.positions()).rows
        filtered_positions = [
            position for position in positions if position.symbol == asset
        ]
        if len(filtered_positions) == 0:
            return None
        position = filtered_positions[0]
        if position.position_qty == 0:
            return None
        is_buy = position.position_qty < 0
        return await self.make_order(
            abs(position.position_qty),
            asset=asset,
            is_buy=is_buy,
            reduce_only=True,
        )

    def make_algo_order(
        self,
        amount,
        price,
        trigger_price,
        asset: PerpetualAssetType = PerpetualAssetType.BTC,
        is_buy=True,
        reduce_only: bool = False,
    ):
        body = dict(
            symbol=asset.value,
            order_quantity=amount,
            order_price=price,
            # algo_type="STOP_LOSS",
            order_type=OrderType.LIMIT,
            # price="0.003",
            # quantity=float(amount),
            # trigger_price_type="MARK_PRICE",
            # trigger_price=trigger_price,
            # reduce_only=reduce_only,
            side="BUY" if is_buy else "SELL",
            order_tag="EMPYREAL",
        )
        response_json = self._send_request("v1/order", body=body, method="POST")
        if response_json["success"]:
            return OrderResponse(**response_json["data"])
        raise ValueError(response_json)

    async def make_limit_order(
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
        response_json = await self._send_request_async(
            "v1/order", body=body, method="POST"
        )
        if response_json["success"]:
            return OrderResponse(**response_json["data"])
        raise ValueError(response_json)

    async def get_order_by_id(
        self,
        order_id: int,
    ):
        response_json = await self._send_request_async(f"v1/order/{order_id}")
        return Order(**response_json["data"])

    async def get_symbol_rules(
        self,
        asset: PerpetualAssetType,
    ):
        return await self._send_request_async(f"v1/public/info/{asset.value}")

    async def make_order(
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

        response_json = await self._send_request_async(
            "v1/order", body=body, method="POST"
        )
        if response_json["success"]:
            return OrderResponse(**response_json["data"])
        raise ValueError(response_json)

    async def _orders(
        self,
        page: int = 1,
        size: int = 100,
        max_pages: int = 3,
        status: str | None = None,
        asset: Optional[PerpetualAssetType] = None,
        start_t: datetime | None = None,
    ):
        if max_pages == 0:
            return []
        if start_t:
            start_time = str(int(start_t.timestamp() * 1000))
        response_json = await self._send_request_async(
            "v1/orders",
            params={
                "page": page,
                "size": size,
                "symbol": asset and asset.value,
                "status": status,
                "start_t": start_t and start_time,
            },
        )

        # 'meta': {'total': 1, 'records_per_page': 25, 'current_page': 1}}
        meta = response_json["data"]["meta"]
        rows = response_json["data"]["rows"]
        if meta["total"] > 25:
            rows += await self._orders(
                page=meta["current_page"] + 1,
                size=size,
                max_pages=max_pages - 1,
                asset=asset,
                status=status,
                start_t=start_t,
            )
        return rows

    async def close_orders(
        self,
        asset: PerpetualAssetType,
    ):
        reponse_json = await self._send_request_async(
            "v1/orders",
            params={
                "symbol": asset.value,
            },
            method="DELETE",
        )
        return reponse_json

    async def close(self, asset: PerpetualAssetType):
        await self.close_position(asset)
        await self.close_orders(asset)

    async def orders(
        self,
        size: int = 100,
        page: int = 1,
        max_pages: int = 3,
        status: Literal["COMPLETED", "INCOMPLETE"] | None = None,
        asset: Optional[PerpetualAssetType] = None,
        start_t: datetime | None = None,
    ) -> list[Order]:
        # TODO: filter by asset type
        orders = await self._orders(
            page=page,
            size=size,
            max_pages=max_pages,
            status=status,
            asset=asset,
            start_t=start_t,
        )
        return [Order(**r) for r in orders]

    def _send_request(self, path, body=None, params=None, method="GET"):
        session = Session()
        res = session.send(
            self._signer.sign_request(
                Request(
                    method,
                    f"{self._BASE_URL}/{path}",
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

    async def _send_request_async(
        self,
        path,
        body: dict | None = None,
        params: dict | None = None,
        method="GET",
    ):
        if params is not None:
            params = {k: v for k, v in params.items() if v}
        if body is not None:
            body = {k: v for k, v in body.items() if v}
        headers = self._signer.build_headers(
            url=f"{self._BASE_URL}/{path}",
            method=method,
            params=params,
            json=body,
        )
        async with httpx.AsyncClient() as client:
            res = await client.request(
                method,
                url=f"{self._BASE_URL}/{path}",
                params=params,
                json=body,
                headers=headers,
                timeout=20,
            )
        try:
            response_json = res.json()
        except Exception as e:
            print(res.text)
            raise e
        if "success" in response_json:
            if not response_json["success"]:
                raise ValueError(response_json)
        if "s" in response_json:
            if not response_json["s"] == "ok":
                raise ValueError(response_json)
        return response_json
