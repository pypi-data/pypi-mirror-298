from enum import Enum


class Status(str, Enum):
    PENDING = "PENDING"  # not supported currently
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"  # not supported currently
    TERMINATED = "TERMINATED"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
