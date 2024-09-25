from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, WrapValidator

from .assets import PerpetualAssetType


class Position(BaseModel):
    symbol: Annotated[
        PerpetualAssetType, WrapValidator(PerpetualAssetType.to_perp_or_unk)
    ]
    position_qty: Decimal
    cost_position: Decimal
    last_sum_unitary_funding: Decimal
    pending_long_qty: Decimal
    pending_short_qty: Decimal
    settle_price: Decimal
    average_open_price: Decimal
    unsettled_pnl: Decimal
    mark_price: Decimal
    est_liq_price: Decimal
    timestamp: datetime
    imr: Decimal
    mmr: Decimal
    IMR_withdraw_orders: Decimal
    MMR_with_orders: Decimal
    pnl_24_h: Decimal
    fee_24_h: Decimal


class PositionData(BaseModel):
    margin_ratio: Decimal
    initial_margin_ratio: Decimal
    maintenance_margin_ratio: Decimal
    open_margin_ratio: Decimal
    current_margin_ratio_with_orders: Decimal
    initial_margin_ratio_with_orders: Decimal
    maintenance_margin_ratio_with_orders: Decimal
    total_collateral_value: Decimal
    free_collateral: Decimal
    rows: list[Position]
    total_pnl_24_h: Decimal
