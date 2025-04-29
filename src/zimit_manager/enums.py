from enum import Enum


class ExecutionStatus(int, Enum):
    FAILED = -1
    REQUESTED = 0
    STOPPED = 1
    PROCESSING = 2
    COMPLETE = 3


class Urgency(int, Enum):
    SAFE = 0
    CONTROVERSIAL = 1
    ENDANGERED = 2
    GONE = 3


class ScopeType(int, Enum):
    UNDEFINED = 0
    DOMAIN = 1
