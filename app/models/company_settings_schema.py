

from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.enums import PayrollCycle


class CompanySettingsCreateRequest(BaseModel):
    salary_payment_day: int = Field(
        ..., ge=1, le=31, description="Day of the month salaries are paid, e.g. 28"
    )
    allow_overtime: bool = Field(True, description="Whether this company pays overtime at all")
    overtime_rate_multiplier: float = Field(1.5, description="Overtime pay multiplier, e.g. 1.5x hourly rate")
    standard_working_days_per_week: int = Field(5, description="e.g. 5 for Mon-Fri, 6 if Saturdays are working days")
    standard_working_hours_per_day: float = Field(8, description="Standard shift length in hours")
    standard_clock_in: str = Field("09:00", description="Default expected clock-in time, 24hr HH:MM")
    standard_clock_out: str = Field("18:00", description="Default expected clock-out time, 24hr HH:MM")
    weekend_days: List[str] = Field(
        default_factory=lambda: ["Saturday", "Sunday"],
        description="Days of the week not counted as working days",
    )
    paid_leaves_allowed_per_month: int = Field(2, description="Default paid leave allowance per employee per month")
    late_arrival_grace_minutes: int = Field(
        0, description="Grace period in minutes before a clock-in is considered late"
    )
    default_payroll_cycle: PayrollCycle = Field(PayrollCycle.MONTHLY, description="Default payroll cycle")


class CompanySettingsUpdateRequest(BaseModel):
  
    salary_payment_day: Optional[int] = Field(None, ge=1, le=31)
    allow_overtime: Optional[bool] = None
    overtime_rate_multiplier: Optional[float] = None
    standard_working_days_per_week: Optional[int] = None
    standard_working_hours_per_day: Optional[float] = None
    standard_clock_in: Optional[str] = None
    standard_clock_out: Optional[str] = None
    weekend_days: Optional[List[str]] = None
    paid_leaves_allowed_per_month: Optional[int] = None
    late_arrival_grace_minutes: Optional[int] = None
    default_payroll_cycle: Optional[PayrollCycle] = None


class CompanySettingsResponse(BaseModel):
    company_id: str
    salary_payment_day: int
    allow_overtime: bool
    overtime_rate_multiplier: float
    standard_working_days_per_week: int
    standard_working_hours_per_day: float
    standard_clock_in: str
    standard_clock_out: str
    weekend_days: List[str]
    paid_leaves_allowed_per_month: int
    late_arrival_grace_minutes: int
    default_payroll_cycle: PayrollCycle
    created_at: str
    updated_at: str
