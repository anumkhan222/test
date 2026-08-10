from datetime import date as date_type
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from app.utils.time_utils import time_str_to_minutes

AttendanceStatus = Literal["Present", "Absent", "Leave"]


class ClockSession(BaseModel):
    clock_in: str = Field(..., description="'HH:MM'")
    clock_out: str = Field(..., description="'HH:MM'")

    @model_validator(mode="after")
    def validate_order(self):
        if time_str_to_minutes(self.clock_out) <= time_str_to_minutes(self.clock_in):
            raise ValueError("clock_out must be after clock_in")
        return self


def _validate_sessions_chronological(sessions: List[ClockSession]):
    for i in range(1, len(sessions)):
        if time_str_to_minutes(sessions[i].clock_in) < time_str_to_minutes(sessions[i - 1].clock_out):
            raise ValueError("clock_sessions must be chronological and non-overlapping")


class AttendanceCreateRequest(BaseModel):
    emp_id: str
    # company_id removed — always taken from the logged-in user's token
    date: date_type
    status: AttendanceStatus
    clock_sessions: List[ClockSession] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_sessions_match_status(self):
        if self.status == "Present":
            if not self.clock_sessions:
                raise ValueError("clock_sessions is required when status is 'Present'")
            _validate_sessions_chronological(self.clock_sessions)
        elif self.clock_sessions:
            raise ValueError("clock_sessions must be empty when status is not 'Present'")
        return self


class AttendanceUpdateRequest(BaseModel):
    status: Optional[AttendanceStatus] = None
    clock_sessions: Optional[List[ClockSession]] = None

    @model_validator(mode="after")
    def validate_sessions_chronological(self):
        if self.clock_sessions:
            _validate_sessions_chronological(self.clock_sessions)
        return self


class AttendanceResponse(BaseModel):
    attendance_id: str
    emp_id: str
    company_id: str
    date: str
    status: AttendanceStatus
    clock_sessions: List[ClockSession] = Field(default_factory=list)
    total_hours_worked: float = 0.0
    late_hours: float = 0.0
    overtime_hours: float = 0.0
    created_at: str
    updated_at: str


class BulkAttendanceItem(BaseModel):
    emp_id: str
    status: AttendanceStatus
    clock_sessions: List[ClockSession] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_sessions_match_status(self):
        if self.status == "Present":
            if not self.clock_sessions:
                raise ValueError("clock_sessions is required when status is 'Present'")
            _validate_sessions_chronological(self.clock_sessions)
        elif self.clock_sessions:
            raise ValueError("clock_sessions must be empty when status is not 'Present'")
        return self


class BulkAttendanceCreateRequest(BaseModel):
    # company_id removed — always taken from the logged-in user's token
    date: date_type
    records: List[BulkAttendanceItem] = Field(..., min_length=1)