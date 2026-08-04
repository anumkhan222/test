from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Query

from app.controllers import attendance_controller
from app.models.attendance_schema import (
    AttendanceCreateRequest,
    AttendanceUpdateRequest,
    AttendanceResponse,
    BulkAttendanceCreateRequest,
)

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


@router.post("/", response_model=AttendanceResponse)
def mark_attendance(payload: AttendanceCreateRequest):
    return attendance_controller.mark_attendance(payload)


@router.post("/bulk")
def mark_bulk_attendance(payload: BulkAttendanceCreateRequest):
    return attendance_controller.mark_bulk_attendance(payload)


@router.get("/", response_model=List[AttendanceResponse])
def list_attendance(
    emp_id: str = Query(..., description="Employee ID"),
    start: Optional[date] = Query(None, description="Range start (YYYY-MM-DD)"),
    end: Optional[date] = Query(None, description="Range end (YYYY-MM-DD)"),
):
    return attendance_controller.list_attendance(emp_id, start, end)


# @router.get("/{attendance_id}", response_model=AttendanceResponse)
# def get_attendance(attendance_id: str):
#     return attendance_controller.get_attendance_record(attendance_id)


# @router.put("/{attendance_id}", response_model=AttendanceResponse)
# def update_attendance(attendance_id: str, payload: AttendanceUpdateRequest):
#     return attendance_controller.update_attendance(attendance_id, payload)


# @router.delete("/{attendance_id}")
# def delete_attendance(attendance_id: str):
#     return attendance_controller.delete_attendance(attendance_id)