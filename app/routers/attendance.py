from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import require_company
from app.controllers import attendance_controller
from app.models.attendance_schema import (
    AttendanceCreateRequest,
    AttendanceUpdateRequest,
    AttendanceResponse,
    BulkAttendanceCreateRequest,
)

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


@router.post("/", response_model=AttendanceResponse)
def mark_attendance(payload: AttendanceCreateRequest, current_user: dict = Depends(require_company)):
    return attendance_controller.mark_attendance(payload, current_user["company_id"])


@router.post("/bulk")
def mark_bulk_attendance(payload: BulkAttendanceCreateRequest, current_user: dict = Depends(require_company)):
    return attendance_controller.mark_bulk_attendance(payload, current_user["company_id"])


@router.get("/", response_model=List[AttendanceResponse])
def list_attendance(
    emp_id: str = Query(...),
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    current_user: dict = Depends(require_company),
):
    return attendance_controller.list_attendance(emp_id, current_user["company_id"], start, end)


# @router.get("/{attendance_id}", response_model=AttendanceResponse)
# def get_attendance(attendance_id: str, current_user: dict = Depends(require_company)):
#     return attendance_controller.get_attendance_record(attendance_id, current_user["company_id"])


# @router.put("/{attendance_id}", response_model=AttendanceResponse)
# def update_attendance(attendance_id: str, payload: AttendanceUpdateRequest, current_user: dict = Depends(require_company)):
#     return attendance_controller.update_attendance(attendance_id, payload, current_user["company_id"])


# @router.delete("/{attendance_id}")
# def delete_attendance(attendance_id: str, current_user: dict = Depends(require_company)):
#     return attendance_controller.delete_attendance(attendance_id, current_user["company_id"])