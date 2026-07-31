
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
