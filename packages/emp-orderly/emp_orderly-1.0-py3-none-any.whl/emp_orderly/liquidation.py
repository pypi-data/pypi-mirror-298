from decimal import Decimal

from pydantic import BaseModel

from emp_orderly_types import PerpetualAssetType, Position


BTC_IMR = Decimal("0.0000003517")
ETH_IMR = Decimal("0.0000003754")
BASE_IMR = Decimal("0.05")
BASE_MMR = Decimal("0.025")
ORDER_FEE = Decimal("0.0006")


class NewOrder(BaseModel):
    qty: Decimal
    symbol: PerpetualAssetType
    price: Decimal


def estimate_liquidation_price(
    positions: list[Position], new_order: NewOrder, total_collateral, mark_price
):
    base_imr = BASE_IMR
    base_mmr = BASE_MMR
    order_fee = ORDER_FEE
    imr_factor = BTC_IMR

    current_position = None
    new_total_mm = Decimal("0")
    new_order_notional = new_order.qty * new_order.price

    for position in positions:
        notional = position.position_qty * position.mark_price
        if new_order.symbol == position.symbol:
            current_position = position
            notional += new_order_notional
        new_total_mm += abs(notional) * position.mmr

    if not current_position:
        new_total_mm += new_order_notional * base_mmr

    new_mmr = max(
        base_mmr,
        (
            base_mmr
            / base_imr
            * imr_factor
            * abs(
                new_order_notional
                + (
                    current_position.position_qty * current_position.mark_price
                    if current_position
                    else Decimal("0")
                )
            )
        )
        ** Decimal("0.8"),
    )

    new_qty: Decimal = new_order.qty + (
        current_position.position_qty if current_position else Decimal("0")
    )
    if new_qty == Decimal("0"):
        return 0

    price: Decimal = Decimal(mark_price) + (
        Decimal(total_collateral) - new_total_mm - order_fee
    ) / (abs(new_qty) * new_mmr - new_qty)

    return price.max(0)
