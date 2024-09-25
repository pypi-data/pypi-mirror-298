from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, WrapValidator

from .assets import PerpetualAssetType


class OrderType(StrEnum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    IOC = "IOC"  # It matches as much as possible at the order_price. If not fully executed, then remaining quantity will be cancelled.
    FOK = "FOK"  # if the order can be fully executed at the order_price then the order gets fully executed otherwise would be cancelled without any execution.
    POST_ONLY = "POST_ONLY"  # if the order will be executed with any maker trades at the time of placement, then it will be cancelled without any execution.
    ASK = "ASK"  # the order price is guranteed to be the best ask price of the orderbook at the time it gets accepted.
    BID = "BID"  # the order price is guranteed to be the best bid price of the orderbook at the time it gets accepted.


class OrderResponse(BaseModel):
    order_id: int
    client_order_id: int | None
    order_type: Literal["LIMIT", "MARKET"]
    order_price: Decimal | None
    order_quantity: Decimal | None
    order_amount: Decimal | None


class Order(BaseModel):
    symbol: Annotated[
        PerpetualAssetType, WrapValidator(PerpetualAssetType.to_perp_or_unk)
    ]
    status: Literal[
        "NEW",
        "CANCELLED",
        "PARTIAL_FILLED",
        "FILLED",
        "REJECTED",
        "INCOMPLETE",
        "COMPLETED",
    ]
    side: Literal["BUY", "SELL"]
    order_id: int
    user_id: int
    price: Decimal | None
    type: Literal["LIMIT", "MARKET"]
    quantity: Decimal
    amount: Decimal | None
    visible: Decimal
    executed: Decimal
    total_fee: Decimal
    fee_asset: str
    client_order_id: str | None
    created_time: datetime
    updated_time: datetime
    average_executed_price: Decimal | None
    reduce_only: bool | None
    order_tag: str | None
    realized_pnl: Decimal

    @property
    def usd_value(self):
        if self.average_executed_price and self.quantity:
            return self.average_executed_price * self.quantity
        return 0
