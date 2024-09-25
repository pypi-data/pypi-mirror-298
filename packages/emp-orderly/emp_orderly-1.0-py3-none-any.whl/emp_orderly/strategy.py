from datetime import datetime
from decimal import Decimal, ROUND_UP
from enum import Enum
from typing import Optional

from pydantic import BaseModel, PrivateAttr

from emp_orderly_types import PerpetualAssetType, MarketInfo, Order, OrderResponse, Position
from emp_orderly.logger import logger
from .account import EmpyrealOrderlySDK
from .sync import EmpyrealOrderlySyncSDK


QUOTE_TICK = {  # price
    PerpetualAssetType.BTC: 1,
    PerpetualAssetType.ETH: 2,
    PerpetualAssetType.WOO: 5,
    PerpetualAssetType.AVAX: 3,
    PerpetualAssetType.MATIC: 4,
    PerpetualAssetType.ARB: 4,
    PerpetualAssetType.INJ: 3,
    PerpetualAssetType.ORDI: 3,
    PerpetualAssetType.SUI: 4,
    PerpetualAssetType.SOL: 3,
    PerpetualAssetType.TIA: 4,
    PerpetualAssetType.LINK: 3,
    PerpetualAssetType.OP: 4,
    PerpetualAssetType.JUP: 4,
    PerpetualAssetType.STRK: 4,
    PerpetualAssetType.BLUR: 4,
    PerpetualAssetType.WIF: 4,
    PerpetualAssetType.W: 3,
    PerpetualAssetType.BNB: 2,
    PerpetualAssetType.WLD: 4,
    PerpetualAssetType.APT: 3,
    PerpetualAssetType.XRP: 4,
    PerpetualAssetType.DOGE: 5,
    PerpetualAssetType.ENA: 3,
    PerpetualAssetType.NEAR: 4,
    PerpetualAssetType.FTM: 4,
    PerpetualAssetType.ETHFI: 3,
    PerpetualAssetType.OMNI: 2,
    PerpetualAssetType.MERL: 4,
    PerpetualAssetType.BCH: 2,
    PerpetualAssetType.ONDO: 4,
    PerpetualAssetType.REZ: 4,
    PerpetualAssetType.SEI: 4,
    PerpetualAssetType.FIL: 3,
    PerpetualAssetType.TON: 3,
    PerpetualAssetType.BOME: 6,
    PerpetualAssetType.MEW: 6,
    PerpetualAssetType.BONK: 6,
    PerpetualAssetType.PEPE: 7,
    PerpetualAssetType.RNDR: 4,
    PerpetualAssetType.NOT: 6,
    PerpetualAssetType.AR: 3,
    PerpetualAssetType.BRETT: 5,
    PerpetualAssetType.IO: 3,
    PerpetualAssetType.ZRO: 3,
    PerpetualAssetType.STG: 4,
    PerpetualAssetType.BLAST: 6,
}

BASE_TICK = {  # amount decimals
    PerpetualAssetType.BTC: '1.00000',
    PerpetualAssetType.ETH: '1.0000',
    PerpetualAssetType.WOO: '1',
    PerpetualAssetType.AVAX: '1.00',
    PerpetualAssetType.MATIC: '1',
    PerpetualAssetType.ARB: '1',
    PerpetualAssetType.INJ: '1.00',
    PerpetualAssetType.ORDI: '1.00',
    PerpetualAssetType.SUI: '1',
    PerpetualAssetType.SOL: '1.00',
    PerpetualAssetType.TIA: '1.0',
    PerpetualAssetType.LINK: '1.00',
    PerpetualAssetType.OP: '1.0',
    PerpetualAssetType.JUP: '1',
    PerpetualAssetType.STRK: '1.0',
    PerpetualAssetType.BLUR: '1',
    PerpetualAssetType.WIF: '1',
    PerpetualAssetType.W: '1.0',
    PerpetualAssetType.BNB: '1.000',
    PerpetualAssetType.WLD: '1.0',
    PerpetualAssetType.APT: '1.0',
    PerpetualAssetType.XRP: '1',
    PerpetualAssetType.DOGE: '1',
    PerpetualAssetType.ENA: '1',
    PerpetualAssetType.NEAR: '1.0',
    PerpetualAssetType.FTM: '1',
    PerpetualAssetType.ETHFI: '1.0',
    PerpetualAssetType.OMNI: '1.00',
    PerpetualAssetType.MERL: '1.0',
    PerpetualAssetType.BCH: '1.000',
    PerpetualAssetType.ONDO: '1',
    PerpetualAssetType.REZ: '1',
    PerpetualAssetType.SEI: '1',
    PerpetualAssetType.FIL: '1.0',
    PerpetualAssetType.TON: '1.0',
    PerpetualAssetType.BOME: '100',
    PerpetualAssetType.MEW: '100',
    PerpetualAssetType.BONK: '1',
    PerpetualAssetType.PEPE: '100',
    PerpetualAssetType.RNDR: '1.0',
    PerpetualAssetType.NOT: '100',
    PerpetualAssetType.AR: '1.0',
    PerpetualAssetType.BRETT: '1',
    PerpetualAssetType.IO: '1.0',
    PerpetualAssetType.ZRO: '1.0',
    PerpetualAssetType.STG: '1',
    PerpetualAssetType.BLAST: '10',
}

class StrategyType(Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    NEUTRAL = "NEUTRAL"


def quantize(d: Decimal, arg: str | Decimal, rounding=ROUND_UP):
    depth = Decimal(arg)
    if float(arg) > 1:
        return (d / depth).quantize(Decimal('1'), rounding) * depth
    return (d).quantize(depth, rounding)


class Sync(BaseModel):
    asset: PerpetualAssetType
    sdk: EmpyrealOrderlySyncSDK
    _asset_info = PrivateAttr(None)

    def orders(self, open: bool = True) -> list[Order]:
        return self.sdk.orders(max_pages=5, asset=self.asset, status='INCOMPLETE' if open else 'COMPLETED')

    def position(self) -> Position | None:
        return self.sdk.position(self.asset)

    def pnl(self, position: Position | None = None) -> Decimal:
        if not position:
            position = self.position()
        return self.calc_pnl(position)

    def close(self):
        self.sdk.close_orders(self.asset)
        self.sdk.close_position(self.asset)

    def get_asset_info(self, force: bool = False) -> MarketInfo:
        if force:
            self._asset_info = self.sdk.get_market_info(self.asset)
        if not self._asset_info:
            self._asset_info = self.sdk.get_market_info(self.asset)
        assert self._asset_info
        return self._asset_info

    def _convert(self, amount: Decimal, mark_price: Decimal | None = None, decimals: int = 4):
        if not mark_price:
            asset_info = self.get_asset_info()
            mark_price = asset_info.mark_price
        return quantize(Decimal(amount) / mark_price, Decimal(decimals), ROUND_UP)

    def to_usd(self, amount: Decimal, mark_price: Decimal | None = None):
        if not mark_price:
            asset_info = self.get_asset_info()
            mark_price = asset_info.mark_price
        return round(Decimal(amount) * mark_price, 4)

    def make_order(self, amount: Decimal, is_buy: bool = True):
        asset_info = self.get_asset_info()
        mark_price = asset_info.mark_price
        asset_amount = round(Decimal(amount) / mark_price, 4)
        return self.sdk.make_order(
            amount=asset_amount,
            asset=self.asset,
            is_buy=is_buy,
        )

    def make_limit_order(
        self,
        amount,
        price: float | Decimal,
        asset: PerpetualAssetType = PerpetualAssetType.BTC,
        is_buy=True,
        reduce_only: bool = False,
    ) -> OrderResponse:
        amount_decimals: str = BASE_TICK.get(asset, '1')
        price_decimals: int = QUOTE_TICK.get(asset, 0)

        asset_info = self.get_asset_info()
        mark_price = asset_info.mark_price
        asset_amount: Decimal = quantize(Decimal(amount) / mark_price, Decimal(amount_decimals))

        rounded_price: float | Decimal = round(price, price_decimals)  # type: ignore
        return self.sdk.make_limit_order(
            amount=asset_amount,
            price=rounded_price,
            asset=asset,
            is_buy=is_buy,
            reduce_only=reduce_only,
        )

    def calc_pnl(self, position: Position | None):
        if not position:
            return Decimal('0')
        return position.position_qty * (position.mark_price - position.average_open_price)


class StrategyBase(BaseModel):
    asset: PerpetualAssetType
    account_id: str
    pvt_hex: str

    stop_loss: Decimal | None = None
    stop_loss_price: Decimal | None = None
    take_profit: Decimal | None = None
    take_profit_price: Decimal | None = None

    _sync: Sync = PrivateAttr()
    _sdk: EmpyrealOrderlySDK = PrivateAttr()
    _asset_info: None | MarketInfo = PrivateAttr(default=None)
    _initialized: bool = PrivateAttr(False)

    @property
    def sync(self):
        return self._sync

    def model_post_init(self, __context) -> None:
        self._sync = Sync(
            asset=self.asset,
            sdk=self._sdk.to_sync(),
        )
        self._asset_info = None

    def calc_pnl(self, position: Position | None):
        if not position:
            return Decimal('0')
        return position.position_qty * (position.mark_price - position.average_open_price)

    def calc_pnl_percentage(self, position: Position | None):
        if not position:
            return Decimal('0')
        return (position.mark_price / position.average_open_price) - Decimal('1')

    async def pnl(self, position: Position | None = None) -> Decimal:
        if not position:
            position = await self.position()
        return self.calc_pnl(position)

    async def pnl_percentage(self) -> Decimal:
        position = await self.position()
        return self.calc_pnl_percentage(position)

    async def _take_profit_price(self, profit_amount: Decimal) -> Optional[Decimal]:
        position = await self.position()
        if not position:
            return None
        quantity, average_open_price = position.position_qty, position.average_open_price
        return (profit_amount / quantity) + average_open_price

    # async def _stop_loss_price(self, stop_loss: Decimal) -> Optional[Decimal]:
    #     position = await self.position()
    #     if not position:
    #         return None
    #     quantity, avg_price = position.position_qty, position.average_open_price
    #     return (-1 * stop_loss) / quantity + avg_price

    async def avg_position_price(self):
        position = await self.position()
        if not position:
            return 0
        return position.average_open_price

    async def est_liq_price(self):
        position = await self.position()
        if not position:
            return 0
        return position.est_liq_price

    async def close(self):
        await self._sdk.close_orders(self.asset)
        await self._sdk.close_position(self.asset)

    async def get_asset_info(self, force: bool = False) -> MarketInfo:
        if force:
            self._asset_info = await self._sdk.get_market_info(self.asset)
        if not self._asset_info:
            self._asset_info = await self._sdk.get_market_info(self.asset)
        assert self._asset_info
        return self._asset_info

    async def orders(self, max_pages: int = 5, open: bool = True, start_t: datetime | None = None) -> list[Order]:
        return await self._sdk.orders(
            max_pages=max_pages,
            asset=self.asset,
            status='INCOMPLETE' if open else 'COMPLETED',
            start_t=start_t,
        )

    async def position(self) -> Position | None:
        return await self._sdk.position(self.asset)

    async def _convert(self, amount: Decimal, mark_price: Decimal | None = None, decimals=4):
        if not mark_price:
            asset_info = await self.get_asset_info()
            mark_price = asset_info.mark_price
        return quantize(Decimal(amount / mark_price), decimals)

    async def to_usd(self, amount: Decimal, mark_price: Decimal | None = None, decimals=4):
        if not mark_price:
            asset_info = await self.get_asset_info()
            mark_price = asset_info.mark_price
        return round(Decimal(amount) * mark_price, decimals)

    async def make_order(self, amount: Decimal, is_buy: bool = True) -> OrderResponse:
        decimals = Decimal(BASE_TICK.get(self.asset, '1.000'))
        asset_info = await self.get_asset_info()
        mark_price = asset_info.mark_price
        asset_amount: Decimal
        if decimals > 1:
            _asset_amount: Decimal = quantize(Decimal(amount) / mark_price, decimals)
            asset_amount = Decimal(round(_asset_amount, -len(str(int(decimals))) + 1)) + decimals
        else:
            asset_amount = quantize(Decimal(amount) / mark_price, decimals, ROUND_UP)
        order = await self._sdk.make_order(
            amount=asset_amount,
            asset=self.asset,
            is_buy=is_buy,
        )
        return order

    async def make_limit_order(
        self,
        amount,
        price: float | Decimal,
        asset: PerpetualAssetType = PerpetualAssetType.BTC,
        is_buy=True,
        reduce_only: bool = False,
    ) -> OrderResponse:
        amount_decimals = BASE_TICK.get(asset, 3)
        price_decimals = QUOTE_TICK.get(asset)

        asset_info = await self.get_asset_info()
        mark_price = asset_info.mark_price

        asset_amount: Decimal = quantize(Decimal(amount) / mark_price, Decimal(amount_decimals), ROUND_UP)

        return await self._sdk.make_limit_order(
            amount=asset_amount,
            price=round(price, price_decimals),
            asset=asset,
            is_buy=is_buy,
            reduce_only=reduce_only,
        )

    async def initialize(self) -> tuple[int, list[OrderResponse]]:
        """This is the init call for a strategy"""
        return 0, []

    async def update(self) -> tuple[bool, list[OrderResponse]]:
        """This is the update call for a strategy"""
        return False, []

    async def refresh(self, refresh_orders: bool = False):
        import asyncio
        if refresh_orders:
            await self._sdk.close_orders(self.asset)
        await asyncio.sleep(1)
        return await self.update()

    def check_boundaries(self, pnl: Decimal) -> bool:
        if self.stop_loss and -self.stop_loss > pnl:
            logger.info(f"Stop Loss: {self.stop_loss} with pnl: {pnl}")
            return True
        if self.take_profit and self.take_profit < pnl:
            logger.info(f"Take Profits: {self.take_profit} with pnl: {pnl}")
            return True
        return False

    def check_price(self, current_price: Decimal, is_long: bool = True) -> bool:
        if not is_long:
            if self.stop_loss_price and self.stop_loss_price < current_price:
                return True
            if self.take_profit_price and current_price < self.take_profit_price:
                return True
            return False

        if self.stop_loss_price and self.stop_loss_price > current_price:
            return True
        if self.take_profit_price and current_price > self.take_profit_price:
            return True
        return False
