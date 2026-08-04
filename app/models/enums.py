
from enum import Enum

class BusinessType(str, Enum):
    INFORMATION_TECHNOLOGY = "Information Technology"
    HEALTHCARE = "Healthcare"
    FINANCE = "Finance"
    RETAIL = "Retail"
    MANUFACTURING = "Manufacturing"
    EDUCATION = "Education"
    REAL_ESTATE = "Real Estate"
    HOSPITALITY = "Hospitality"
    CONSTRUCTION = "Construction"
    TRANSPORTATION = "Transportation"
    OTHER = "Other"


class BusinessSize(str, Enum):
    SIZE_1_50 = "1-50 employees"
    SIZE_51_200 = "51-200 employees"
    SIZE_201_500 = "201-500 employees"
    SIZE_501_1000 = "501-1000 employees"
    SIZE_1000_PLUS = "1000+ employees"



class PayrollCycle(str, Enum):
    MONTHLY = "Monthly"
    WEEKLY = "Weekly"



class Department(str, Enum):
    FRONTEND = "Frontend"
    BACKEND = "Backend"
    UI_UX = "UI/UX"
    OTHER = "Other"


class SalaryType(str, Enum):
    MONTHLY = "Monthly"
    HOURLY = "Hourly"


class PaymentMethod(str, Enum):
    BANK_TRANSFER = "Bank Transfer"
    CASH = "Cash"
    CHEQUE = "Cheque"


class AmountType(str, Enum):
    FIXED = "Fixed"
    PERCENTAGE = "Percentage"
