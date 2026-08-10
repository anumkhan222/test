from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from app.models.enums import Department, SalaryType, PaymentMethod, AmountType, PayrollCycle


class DeductionRule(BaseModel):
    deduction_type: str
    amount_type: AmountType
    amount: float


class AllowanceRule(BaseModel):
    allowance_type: str
    amount_type: AmountType
    amount: float


class SalaryRule(BaseModel):
    base_salary: float = Field(..., gt=0)
    pay_period: PayrollCycle = Field(PayrollCycle.MONTHLY)
    payment_method: PaymentMethod = Field(PaymentMethod.BANK_TRANSFER)
    currency: str = Field("USD")
    include_allowance_and_overtime_in_payroll: bool = Field(True)
    standard_working_days_per_month: Optional[int] = None
    standard_hours_per_day: Optional[float] = None
    standard_clock_in: Optional[str] = None
    standard_clock_out: Optional[str] = None
    paid_leaves_allowed_per_month: Optional[int] = None
    overtime_rate_multiplier: Optional[float] = None
    weekend_days: Optional[List[str]] = None


# Partial version — every field optional, used ONLY for updates so we can
# merge just the fields the user actually sent onto the existing document.
class SalaryRuleUpdate(BaseModel):
    base_salary: Optional[float] = Field(None, gt=0)
    pay_period: Optional[PayrollCycle] = None
    payment_method: Optional[PaymentMethod] = None
    currency: Optional[str] = None
    include_allowance_and_overtime_in_payroll: Optional[bool] = None
    standard_working_days_per_month: Optional[int] = None
    standard_hours_per_day: Optional[float] = None
    standard_clock_in: Optional[str] = None
    standard_clock_out: Optional[str] = None
    paid_leaves_allowed_per_month: Optional[int] = None
    overtime_rate_multiplier: Optional[float] = None
    weekend_days: Optional[List[str]] = None


class EmployeeCreateRequest(BaseModel):
    
    emp_name: str = Field(..., min_length=1)
    email: EmailStr
    profile_image: Optional[str] = None
    department: Department
    designation: str = Field(..., min_length=1)
    salary_type: SalaryType
    salary_rule: SalaryRule
    deduction_rules: List[DeductionRule] = Field(default_factory=list)
    allowance_rules: List[AllowanceRule] = Field(default_factory=list)


class EmployeeUpdateRequest(BaseModel):
    emp_name: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_image: Optional[str] = None
    department: Optional[Department] = None
    designation: Optional[str] = None
    salary_type: Optional[SalaryType] = None
    salary_rule: Optional[SalaryRuleUpdate] = None   # <-- partial now, not full SalaryRule
    deduction_rules: Optional[List[DeductionRule]] = None
    allowance_rules: Optional[List[AllowanceRule]] = None


class EmployeeResponse(BaseModel):
    emp_id: str
    company_id: str
    emp_name: str
    email: EmailStr
    profile_image: Optional[str] = None
    department: Department
    designation: str
    salary_type: SalaryType
    salary_rule: SalaryRule
    deduction_rules: List[DeductionRule]
    allowance_rules: List[AllowanceRule]
    created_at: str
    updated_at: str