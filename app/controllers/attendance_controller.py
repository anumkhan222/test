from datetime import date, datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException

from app.config import database
from app.controllers import employee_controller
from app.models.attendance_schema import (
    AttendanceCreateRequest,
    AttendanceUpdateRequest,
    BulkAttendanceCreateRequest,
)
from app.utils.time_utils import time_str_to_hours, count_working_days


def _to_object_id(attendance_id: str) -> ObjectId:
    try:
        return ObjectId(attendance_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail=f"'{attendance_id}' is not a valid attendance_id")


def _calc_hours(employee: dict, status: str, clock_sessions: list):
    if status != "Present" or not clock_sessions:
        return 0.0, 0.0, 0.0

    policy = employee["salary_rule"]
    standard_clock_in = policy.get("standard_clock_in") or "09:00"
    standard_clock_out = policy.get("standard_clock_out") or "18:00"

    first_clock_in = clock_sessions[0]["clock_in"]
    last_clock_out = clock_sessions[-1]["clock_out"]

    total_hours_worked = round(
        sum(time_str_to_hours(s["clock_out"]) - time_str_to_hours(s["clock_in"]) for s in clock_sessions), 2
    )
    late_hours = max(0.0, round(time_str_to_hours(first_clock_in) - time_str_to_hours(standard_clock_in), 2))
    overtime_hours = max(0.0, round(time_str_to_hours(last_clock_out) - time_str_to_hours(standard_clock_out), 2))

    return total_hours_worked, late_hours, overtime_hours


def _build_record(employee: dict, company_id: str, date_str: str, status: str, clock_sessions: list) -> dict:
    total_hours_worked, late_hours, overtime_hours = _calc_hours(employee, status, clock_sessions)
    now = datetime.now(timezone.utc).isoformat()

    return {
        "emp_id": employee["emp_id"],
        "company_id": company_id,
        "date": date_str,
        "status": status,
        "clock_sessions": clock_sessions,
        "total_hours_worked": total_hours_worked,
        "late_hours": late_hours,
        "overtime_hours": overtime_hours,
        "created_at": now,
        "updated_at": now,
    }


# mark attendance for one employee on one date. company_id comes from the logged-in
def mark_attendance(payload: AttendanceCreateRequest, company_id: str) -> dict:

    employee = employee_controller.get_employee_or_none(payload.emp_id)
    if employee is None or employee["company_id"] != company_id:
        raise HTTPException(status_code=404, detail=f"Employee '{payload.emp_id}' not found in your company")

    date_str = payload.date.isoformat()

    if database.attendance_collection.find_one({"emp_id": payload.emp_id, "date": date_str}):
        raise HTTPException(
            status_code=409,
            detail=f"Attendance for employee '{payload.emp_id}' on '{date_str}' already exists. Use PUT to update it.",
        )

    clock_sessions = [s.model_dump(mode="json") for s in payload.clock_sessions]
    doc = _build_record(employee, company_id, date_str, payload.status, clock_sessions)

    database.attendance_collection.insert_one(doc)
    doc["attendance_id"] = str(doc.pop("_id"))
    return doc


def mark_bulk_attendance(payload: BulkAttendanceCreateRequest, company_id: str) -> dict:

    date_str = payload.date.isoformat()
    created, skipped = [], []

    for item in payload.records:
        employee = employee_controller.get_employee_or_none(item.emp_id)

        if employee is None or employee["company_id"] != company_id:
            skipped.append({"emp_id": item.emp_id, "reason": "Employee not found in your company"})
            continue

        if database.attendance_collection.find_one({"emp_id": item.emp_id, "date": date_str}):
            skipped.append({"emp_id": item.emp_id, "reason": "Attendance already exists for this date"})
            continue

        clock_sessions = [s.model_dump(mode="json") for s in item.clock_sessions]
        doc = _build_record(employee, company_id, date_str, item.status, clock_sessions)
        database.attendance_collection.insert_one(doc)
        doc["attendance_id"] = str(doc.pop("_id"))
        created.append(doc)

    return {"created": created, "skipped": skipped}


def get_attendance_record(attendance_id: str, company_id: str) -> dict:
    doc = database.attendance_collection.find_one({"_id": _to_object_id(attendance_id)})
    if not doc or doc["company_id"] != company_id:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    doc["attendance_id"] = str(doc.pop("_id"))
    return doc


def list_attendance(emp_id: str, company_id: str, start: date | None = None, end: date | None = None) -> list:
    query = {"emp_id": emp_id, "company_id": company_id}
    if start and end:
        query["date"] = {"$gte": start.isoformat(), "$lte": end.isoformat()}
    docs = list(database.attendance_collection.find(query).sort("date", 1))
    for doc in docs:
        doc["attendance_id"] = str(doc.pop("_id"))
    return docs


def update_attendance(attendance_id: str, payload: AttendanceUpdateRequest, company_id: str) -> dict:

    existing = get_attendance_record(attendance_id, company_id)

    employee = employee_controller.get_employee_or_none(existing["emp_id"])
    if employee is None:
        raise HTTPException(status_code=404, detail=f"Employee '{existing['emp_id']}' not found")

    status = payload.status if payload.status is not None else existing["status"]

    if payload.clock_sessions is not None:
        clock_sessions = [s.model_dump(mode="json") for s in payload.clock_sessions]
    else:
        clock_sessions = existing.get("clock_sessions", [])

    if status != "Present":
        clock_sessions = []
    elif not clock_sessions:
        raise HTTPException(status_code=400, detail="clock_sessions is required when status is 'Present'")

    total_hours_worked, late_hours, overtime_hours = _calc_hours(employee, status, clock_sessions)

    update_fields = {
        "status": status,
        "clock_sessions": clock_sessions,
        "total_hours_worked": total_hours_worked,
        "late_hours": late_hours,
        "overtime_hours": overtime_hours,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    database.attendance_collection.update_one({"_id": _to_object_id(attendance_id)}, {"$set": update_fields})
    return get_attendance_record(attendance_id, company_id)


def delete_attendance(attendance_id: str, company_id: str) -> dict:
    get_attendance_record(attendance_id, company_id)
    database.attendance_collection.delete_one({"_id": _to_object_id(attendance_id)})
    return {"message": f"Attendance record '{attendance_id}' deleted successfully"}


# no company_id scoping needed here — called internally by payroll_controller,
# which has already verified the employee belongs to the caller's company.
def get_attendance_summary(emp_id: str, pay_period_start: date, pay_period_end: date) -> dict:

    employee = employee_controller.get_employee_or_none(emp_id)
    weekend_days = (employee["salary_rule"].get("weekend_days") if employee else None) or ["Saturday", "Sunday"]
    working_days = count_working_days(pay_period_start, pay_period_end, weekend_days)

    pipeline = [
        {"$match": {
            "emp_id": emp_id,
            "date": {"$gte": pay_period_start.isoformat(), "$lte": pay_period_end.isoformat()},
        }},
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1},
            "overtime_hours": {"$sum": "$overtime_hours"},
            "late_hours": {"$sum": "$late_hours"},
        }},
    ]

    results = list(database.attendance_collection.aggregate(pipeline))

    present_days = 0
    leave_days = 0
    overtime_hours = 0.0
    late_arrival_hours = 0.0

    for r in results:
        if r["_id"] == "Present":
            present_days = r["count"]
            overtime_hours = round(r["overtime_hours"], 2)
            late_arrival_hours = round(r["late_hours"], 2)
        elif r["_id"] == "Leave":
            leave_days = r["count"]

    absent_days = max(0, working_days - present_days - leave_days)

    return {
        "working_days": working_days,
        "present_days": present_days,
        "leave_days": leave_days,
        "absent_days": absent_days,
        "overtime_hours": overtime_hours,
        "late_arrival_hours": late_arrival_hours,
    }