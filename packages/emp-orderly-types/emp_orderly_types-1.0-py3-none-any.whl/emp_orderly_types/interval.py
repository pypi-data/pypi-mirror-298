from enum import StrEnum


class Interval(StrEnum):
    """Timeframe Intervals for trading view"""

    minute = "1"
    five_minute = "5"
    fifteen_minute = "15"
    thirty_minute = "30"
    hour = "60"
    four_hour = "4h"
    twelve_hour = "12h"
    day = "1D"
