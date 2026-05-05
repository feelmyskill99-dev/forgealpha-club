from enum import Enum, IntEnum


class Tier(IntEnum):
    FREE = 0
    BASIC = 1
    VIP = 2
    PRO = 3


class PaymentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    EXPIRED = "expired"
    REFUNDED = "refunded"


TIER_NAMES = {
    Tier.FREE: "Free",
    Tier.BASIC: "Basic",
    Tier.VIP: "VIP",
    Tier.PRO: "Pro",
}