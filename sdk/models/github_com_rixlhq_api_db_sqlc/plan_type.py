from enum import Enum

class PlanType(str, Enum):
    Free = "free",
    Pro = "pro",
    Custom = "custom",
    Pay_as_you_go = "pay_as_you_go",

