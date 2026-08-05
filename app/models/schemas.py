

from datetime import date
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, model_validator

from app.models.enums import PayrollCycle, SalaryType, Department


PERIOD_LENGTH_RULES = {
    "Weekly": {"min_days": 6, "max_days": 8},
    "Monthly": {"min_days": 27, "max_days": 31},
}


class GeneratePayrollRequest(BaseModel):
    payroll_type: PayrollCycle = Field(
        ..., description="Whether this payroll batch is Monthly or Weekly"
    )
    pay_period_start: date = Field(..., description="Start date of the pay period")
    pay_period_end: date = Field(..., description="End date of the pay period")
    emp_type: SalaryType = Field(
        ..., description="Employee salary type this payroll run applies to"
    )
    company_id: Optional[str] = Field(
        None, description="Optional filter — only include employees from this company"
    )
    department: Optional[Department] = Field(
        None, description="Optional filter — only include employees from this department"
    )
    employee_ids: List[str] = Field(
        ..., min_length=1, description="List of employee IDs to include in this payroll run"
    )

    @model_validator(mode="after")
    def validate_period_matches_payroll_type(self):
        if self.pay_period_end < self.pay_period_start:
            raise ValueError("pay_period_end cannot be before pay_period_start")

        span_days = (self.pay_period_end - self.pay_period_start).days + 1
        rule = PERIOD_LENGTH_RULES[self.payroll_type.value]

        if not (rule["min_days"] <= span_days <= rule["max_days"]):
            raise ValueError(
                f"payroll_type '{self.payroll_type.value}' expects a pay period of "
                f"{rule['min_days']}-{rule['max_days']} days, but the given range "
                f"({self.pay_period_start} to {self.pay_period_end}) is {span_days} days."
            )
        return self


class PayrollComponent(BaseModel):
    component: str
    type: Literal["Earnings", "Deduction"]
    amount: float


class AttendanceSummary(BaseModel):
    working_days: int
    present_days: int
    absent_days: int
    paid_leaves_allowed: int
    overtime_hours: float
    late_arrival_hours: float

class EmployeePayroll(BaseModel):
    emp_id: str
    emp_name: str
    email: str
    profile_image: Optional[str] = None
    department: str
    designation: str
    status: str
    payroll_calculation: List[PayrollComponent]
    attendance_summary: AttendanceSummary
    gross_salary: float
    total_earnings: float
    total_deductions: float
    total_allowance: float
    net_salary: float
    deduction_shortfall: float


class GeneratePayrollResponse(BaseModel):
    payroll_batch_id: str
    payroll_type: str
    pay_period: dict
    generated_at: str
    employees_payroll: List[EmployeePayroll]
    skipped_employees: Optional[List[dict]] = None
