from datetime import date as date_type
from typing import List, Optional

from pydantic import BaseModel, Field


class AttendanceCreateRequest(BaseModel):
    emp_id: str = Field(..., description="Employee this record belongs to")
    company_id: str = Field(..., description="Must match the employee's company_id")
    date: date_type = Field(..., description="The calendar date this record is for")
    clock_in: str = Field(..., description="'HH:MM' actual clock-in time")
    clock_out: str = Field(..., description="'HH:MM' actual clock-out time")


class AttendanceUpdateRequest(BaseModel):
    clock_in: Optional[str] = None
    clock_out: Optional[str] = None


class AttendanceResponse(BaseModel):
    attendance_id: str
    emp_id: str
    company_id: str
    date: str
    clock_in: str
    clock_out: str
    late_hours: float
    overtime_hours: float
    created_at: str
    updated_at: str


class BulkAttendanceItem(BaseModel):
    emp_id: str
    clock_in: str
    clock_out: str


class BulkAttendanceCreateRequest(BaseModel):
    company_id: str
    date: date_type = Field(..., description="The calendar date these records are for")
    records: List[BulkAttendanceItem] = Field(..., min_length=1)