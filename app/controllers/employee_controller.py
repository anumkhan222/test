from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException

from app.config import database
from app.controllers import company_controller
from app.models.employee_schema import EmployeeCreateRequest, EmployeeUpdateRequest


def _to_object_id(emp_id: str) -> ObjectId:
    try:
        return ObjectId(emp_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail=f"'{emp_id}' is not a valid emp_id")


def _get_company_settings_or_none(company_id: str):
    try:
        return company_controller.get_settings(company_id)
    except HTTPException:
        return None


def _resolve_attendance_policy(salary_rule: dict, settings: dict | None) -> dict:
    weekly_days = settings["standard_working_days_per_week"] if settings else 5
    computed_monthly_days = round(weekly_days * 52 / 12)

    return {
        "standard_working_days_per_month": salary_rule.get("standard_working_days_per_month")
        or computed_monthly_days,
        "standard_hours_per_day": salary_rule.get("standard_hours_per_day")
        or (settings["standard_working_hours_per_day"] if settings else 8),
        "standard_clock_in": salary_rule.get("standard_clock_in")
        or (settings["standard_clock_in"] if settings else "09:00"),
        "standard_clock_out": salary_rule.get("standard_clock_out")
        or (settings["standard_clock_out"] if settings else "18:00"),
        "paid_leaves_allowed_per_month": (
            salary_rule["paid_leaves_allowed_per_month"]
            if salary_rule.get("paid_leaves_allowed_per_month") is not None
            else (settings["paid_leaves_allowed_per_month"] if settings else 2)
        ),
    }


def create_employee(payload: EmployeeCreateRequest) -> dict:

    company_controller.get_company(payload.company_id)
    settings = _get_company_settings_or_none(payload.company_id)

    now = datetime.now(timezone.utc).isoformat()

    employee_doc = payload.model_dump(mode="json")
    employee_doc["created_at"] = now
    employee_doc["updated_at"] = now

    employee_doc["salary_rule"].update(_resolve_attendance_policy(employee_doc["salary_rule"], settings))

    database.employees_collection.insert_one(employee_doc)  

    employee_doc["emp_id"] = str(employee_doc.pop("_id"))
    return employee_doc


def get_employees(
    company_id: str,
    emp_id: str | None = None,
    department: str | None = None,
    salary_type: str | None = None,
    pay_period: str | None = None,
):
    filters = {"company_id": company_id}

    # Filter by employee id
    if emp_id is not None:
        filters["_id"] = _to_object_id(emp_id)

    # Filter by department
    if department is not None:
        filters["department"] = department

    # Filter by salary type
    if salary_type is not None:
        filters["salary_type"] = salary_type

    # Filter by pay period
    if pay_period is not None:
        filters["pay_period"] = pay_period

    docs = list(database.employees_collection.find(filters))

    if emp_id is not None:
        if not docs:
            raise HTTPException(
                status_code=404,
                detail=f"Employee '{emp_id}' not found"
            )

        doc = docs[0]
        doc["emp_id"] = str(doc.pop("_id"))
        return doc

    for doc in docs:
        doc["emp_id"] = str(doc.pop("_id"))

    return docs


def update_employee(emp_id: str, payload: EmployeeUpdateRequest) -> dict:

    existing = database.employees_collection.find_one(
        {"_id": _to_object_id(emp_id)}
    )

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail=f"Employee '{emp_id}' not found"
        )

    existing["emp_id"] = str(existing.pop("_id"))

    update_fields = {}

    if payload.emp_name is not None:
        update_fields["emp_name"] = payload.emp_name

    if payload.email is not None:
        update_fields["email"] = payload.email

    if payload.profile_image is not None:
        update_fields["profile_image"] = payload.profile_image

    if payload.department is not None:
        update_fields["department"] = payload.department.value

    if payload.designation is not None:
        update_fields["designation"] = payload.designation

    if payload.salary_type is not None:
        update_fields["salary_type"] = payload.salary_type.value

    if payload.salary_rule is not None:
        update_fields["salary_rule"] = payload.salary_rule.model_dump(mode="json")

    if payload.deduction_rules is not None:
        update_fields["deduction_rules"] = [
            d.model_dump(mode="json") for d in payload.deduction_rules
        ]

    if payload.allowance_rules is not None:
        update_fields["allowance_rules"] = [
            a.model_dump(mode="json") for a in payload.allowance_rules
        ]

    update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()

    database.employees_collection.update_one(
        {"_id": _to_object_id(emp_id)},
        {"$set": update_fields},
    )

    return get_employees(
        company_id=existing["company_id"],
        emp_id=emp_id,
    )

def delete_employee(emp_id: str) -> dict:

    existing = database.employees_collection.find_one(
        {"_id": _to_object_id(emp_id)}
    )

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail=f"Employee '{emp_id}' not found"
        )

    database.employees_collection.delete_one(
        {"_id": _to_object_id(emp_id)}
    )

    return {
        "message": f"Employee '{emp_id}' deleted successfully"
    } 
    
def get_employee_or_none(emp_id: str):
    object_id = _to_object_id(emp_id)

    doc = database.employees_collection.find_one({"_id": object_id})

    if doc:
        doc["emp_id"] = str(doc.pop("_id"))

    return doc