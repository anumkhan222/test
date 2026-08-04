from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from app.models.enums import Department, SalaryType, PaymentMethod, AmountType, PayrollCycle


class DeductionRule(BaseModel):
    deduction_type: str = Field(..., description="e.g. 'UIF', 'Income Tax' — free text, company-configurable")
    amount_type: AmountType
    amount: float = Field(..., description="If Fixed: a flat amount. If Percentage: a % of gross salary.")


class AllowanceRule(BaseModel):
    allowance_type: str = Field(..., description="e.g. 'Pick and Drop', 'Expenses' — free text, company-configurable")
    amount_type: AmountType
    amount: float = Field(..., description="If Fixed: a flat amount. If Percentage: a % of gross salary.")


class SalaryRule(BaseModel):
    base_salary: float = Field(..., gt=0, description="Monthly salary amount, or hourly rate if salary_type is Hourly")
    pay_period: PayrollCycle = Field(PayrollCycle.MONTHLY, description="How often this employee is paid")
    payment_method: PaymentMethod = Field(PaymentMethod.BANK_TRANSFER)
    currency: str = Field("USD", description="Currency code for this employee's pay")
    include_allowance_and_overtime_in_payroll: bool = Field(True)
    standard_working_days_per_month: Optional[int] = None
    standard_hours_per_day: Optional[float] = None
    standard_clock_in: Optional[str] = None
    standard_clock_out: Optional[str] = None
    paid_leaves_allowed_per_month: Optional[int] = None


class EmployeeCreateRequest(BaseModel):
    company_id: str = Field(..., description="The company this employee belongs to — must already exist")
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
    salary_rule: Optional[SalaryRule] = None
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