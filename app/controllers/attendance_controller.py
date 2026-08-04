from datetime import date, datetime, timedelta, timezone

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


def _to_object_id(attendance_id: str) -> ObjectId:
    try:
        return ObjectId(attendance_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail=f"'{attendance_id}' is not a valid attendance_id")

# convert time into hours for calculation
def _time_str_to_hours(time_str: str) -> float:
    t = datetime.strptime(time_str, "%H:%M")
    return t.hour + (t.minute / 60)

# calculate late and overtime hours
def _calc_late_and_overtime(employee: dict, clock_in: str, clock_out: str):
    policy = employee["salary_rule"]
    standard_clock_in = policy.get("standard_clock_in") or "09:00"
    standard_clock_out = policy.get("standard_clock_out") or "18:00"

    late_hours = max(0.0, round(_time_str_to_hours(clock_in) - _time_str_to_hours(standard_clock_in), 2))
    overtime_hours = max(0.0, round(_time_str_to_hours(clock_out) - _time_str_to_hours(standard_clock_out), 2))
    return late_hours, overtime_hours

# create an attendance record
def _build_record(employee: dict, company_id: str, date_str: str, clock_in: str, clock_out: str) -> dict:
    late_hours, overtime_hours = _calc_late_and_overtime(employee, clock_in, clock_out)
    now = datetime.now(timezone.utc).isoformat()

    return {
        "emp_id": employee["emp_id"],
        "company_id": company_id,
        "date": date_str,
        "clock_in": clock_in,
        "clock_out": clock_out,
        "late_hours": late_hours,
        "overtime_hours": overtime_hours,
        "created_at": now,
        "updated_at": now,
    }



def mark_attendance(payload: AttendanceCreateRequest) -> dict:

    employee = employee_controller.get_employee_or_none(payload.emp_id)
    if employee is None:
        raise HTTPException(status_code=404, detail=f"Employee '{payload.emp_id}' not found")

    if employee["company_id"] != payload.company_id:
        raise HTTPException(status_code=400, detail="Employee does not belong to the given company_id")

    date_str = payload.date.isoformat()

    if database.attendance_collection.find_one({"emp_id": payload.emp_id, "date": date_str}):
        raise HTTPException(
            status_code=409,
            detail=f"Attendance for employee '{payload.emp_id}' on '{date_str}' already exists. Use PUT to update it.",
        )

    doc = _build_record(employee, payload.company_id, date_str, payload.clock_in, payload.clock_out)

    database.attendance_collection.insert_one(doc)
    doc["attendance_id"] = str(doc.pop("_id"))
    return doc


# mark attendance for many employees on the same date in one call
def mark_bulk_attendance(payload: BulkAttendanceCreateRequest) -> dict:

    date_str = payload.date.isoformat()
    created = []
    skipped = []

    for item in payload.records:
        employee = employee_controller.get_employee_or_none(item.emp_id)

        if employee is None:
            skipped.append({"emp_id": item.emp_id, "reason": "Employee not found"})
            continue

        if employee["company_id"] != payload.company_id:
            skipped.append({"emp_id": item.emp_id, "reason": "Employee does not belong to this company_id"})
            continue

        if database.attendance_collection.find_one({"emp_id": item.emp_id, "date": date_str}):
            skipped.append({"emp_id": item.emp_id, "reason": "Attendance already exists for this date"})
            continue

        doc = _build_record(employee, payload.company_id, date_str, item.clock_in, item.clock_out)
        database.attendance_collection.insert_one(doc)
        doc["attendance_id"] = str(doc.pop("_id"))
        created.append(doc)

    return {"created": created, "skipped": skipped}


def get_attendance_record(attendance_id: str) -> dict:
    doc = database.attendance_collection.find_one({"_id": _to_object_id(attendance_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    doc["attendance_id"] = str(doc.pop("_id"))
    return doc


def list_attendance(emp_id: str, start: date | None = None, end: date | None = None) -> list:
    query = {"emp_id": emp_id}
    if start and end:
        query["date"] = {"$gte": start.isoformat(), "$lte": end.isoformat()}

    docs = list(database.attendance_collection.find(query).sort("date", 1))
    for doc in docs:
        doc["attendance_id"] = str(doc.pop("_id"))
    return docs


def update_attendance(attendance_id: str, payload: AttendanceUpdateRequest) -> dict:

    existing = get_attendance_record(attendance_id)

    employee = employee_controller.get_employee_or_none(existing["emp_id"])
    if employee is None:
        raise HTTPException(status_code=404, detail=f"Employee '{existing['emp_id']}' not found")

    clock_in = payload.clock_in if payload.clock_in is not None else existing["clock_in"]
    clock_out = payload.clock_out if payload.clock_out is not None else existing["clock_out"]

    late_hours, overtime_hours = _calc_late_and_overtime(employee, clock_in, clock_out)

    update_fields = {
        "clock_in": clock_in,
        "clock_out": clock_out,
        "late_hours": late_hours,
        "overtime_hours": overtime_hours,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    database.attendance_collection.update_one({"_id": _to_object_id(attendance_id)}, {"$set": update_fields})
    return get_attendance_record(attendance_id)


def delete_attendance(attendance_id: str) -> dict:
    get_attendance_record(attendance_id)
    database.attendance_collection.delete_one({"_id": _to_object_id(attendance_id)})
    return {"message": f"Attendance record '{attendance_id}' deleted successfully"}


def _count_weekdays(start: date, end: date) -> int:
    total_days = (end - start).days + 1
    return sum(1 for i in range(total_days) if (start + timedelta(days=i)).weekday() < 5)



def get_attendance_summary(emp_id: str, pay_period_start: date, pay_period_end: date) -> dict:

    working_days = _count_weekdays(pay_period_start, pay_period_end)

    pipeline = [
        {
            "$match": {
                "emp_id": emp_id,
                "date": {
                    "$gte": pay_period_start.isoformat(),
                    "$lte": pay_period_end.isoformat(),
                },
            }
        },
        {
            "$group": {
                "_id": "$emp_id",
                "present_days": {"$sum": 1},
                "overtime_hours": {"$sum": "$overtime_hours"},
                "late_arrival_hours": {"$sum": "$late_hours"},
            }
        },
    ]

    result = list(database.attendance_collection.aggregate(pipeline))

    if not result:
        present_days = 0
        overtime_hours = 0.0
        late_arrival_hours = 0.0
    else:
        present_days = result[0]["present_days"]
        overtime_hours = round(result[0]["overtime_hours"], 2)
        late_arrival_hours = round(result[0]["late_arrival_hours"], 2)

    absent_days = max(0, working_days - present_days)

    return {
        "working_days": working_days,
        "present_days": present_days,
        "absent_days": absent_days,
        "overtime_hours": overtime_hours,
        "late_arrival_hours": late_arrival_hours,
    }