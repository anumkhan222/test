from datetime import date
from typing import List, Optional, Literal

from pydantic import BaseModel, Field, model_validator


# valid pay period length for each payroll type
PERIOD_LENGTH_RULES = {
    "Weekly": {"min_days": 6, "max_days": 8},
    "Monthly": {"min_days": 27, "max_days": 31},
}


# request model for generating payroll
class GeneratePayrollRequest(BaseModel):

    payroll_type: Literal["Monthly", "Weekly"] = Field(
        ..., description="Whether this payroll batch is Monthly or Weekly"
    )

    pay_period_start: date = Field(
        ..., description="Start date of the pay period"
    )

    pay_period_end: date = Field(
        ..., description="End date of the pay period"
    )

    emp_type: Literal["Monthly", "Weekly", "Hourly"] = Field(
        ..., description="Employee salary type this payroll run applies to"
    )

    department: Optional[Literal["Frontend", "Backend", "UI/UX"]] = Field(
        None,
        description="Optional filter — only include employees from this department",
    )

    employee_ids: List[str] = Field(
        ...,
        min_length=1,
        description="List of employee IDs to include in this payroll run",
    )

    #validate pay period based on payroll type
    @model_validator(mode="after")
    def validate_period_matches_payroll_type(self):

        #Make sure that end date is after start date
        if self.pay_period_end < self.pay_period_start:
            raise ValueError(
                "pay_period_end cannot be before pay_period_start"
            )

        #calculate total days in the pay period
        span_days = (
            self.pay_period_end - self.pay_period_start
        ).days + 1

        # get allowed day range for payroll type.
        rule = PERIOD_LENGTH_RULES[self.payroll_type]

        #check if pay period length is valid.
        if not (rule["min_days"] <= span_days <= rule["max_days"]):
            raise ValueError(
                f"payroll_type '{self.payroll_type}' expects a pay period of "
                f"{rule['min_days']}-{rule['max_days']} days, but the given range "
                f"({self.pay_period_start} to {self.pay_period_end}) is {span_days} days."
            )

        return self


# Model for one payroll.
class PayrollComponent(BaseModel):
    component: str
    type: Literal["Earnings", "Deduction"]
    amount: float


# model for employee attendance
class AttendanceSummary(BaseModel):
    working_days: int
    present_days: int
    leaves: int
    absent_days: int
    overtime_hours: float
    late_arrival_hours: float


#model for one employees
class EmployeePayroll(BaseModel):
    emp_id: str
    emp_name: str
    email: str
    profile_image: str
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


# response model for payroll generation API
class GeneratePayrollResponse(BaseModel):
    payroll_batch_id: str
    payroll_type: str
    pay_period: dict
    generated_at: str
    employees_payroll: List[EmployeePayroll]
    skipped_employees: Optional[List[dict]] = None