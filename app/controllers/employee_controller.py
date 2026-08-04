

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

    database.employees_collection.insert_one(employee_doc)  # fills in employee_doc["_id"]

    employee_doc["emp_id"] = str(employee_doc.pop("_id"))
    return employee_doc


def get_employees(company_id: str, emp_id: str = None):

    # Return one employee if emp_id is provided
    if emp_id:
        return get_employee(company_id, emp_id)

    # Otherwise return all employees of the company
    return get_all_employees(company_id)

def get_employee_or_none(emp_id: str):

    try:
        object_id = _to_object_id(emp_id)
    except HTTPException:
        return None

    doc = database.employees_collection.find_one({"_id": object_id})
    if doc:
        doc["emp_id"] = str(doc.pop("_id"))
    return doc


def update_employee(emp_id: str, payload: EmployeeUpdateRequest) -> dict:

    get_employee(emp_id)  

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
        update_fields["deduction_rules"] = [d.model_dump(mode="json") for d in payload.deduction_rules]
    if payload.allowance_rules is not None:
        update_fields["allowance_rules"] = [a.model_dump(mode="json") for a in payload.allowance_rules]
    if payload.attendance_events is not None:
        update_fields["attendance_events"] = payload.attendance_events.model_dump(mode="json")

    update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()

    database.employees_collection.update_one({"_id": _to_object_id(emp_id)}, {"$set": update_fields})
    return get_employee(emp_id)


def delete_employee(emp_id: str) -> dict:

    get_employee(emp_id)  
    database.employees_collection.delete_one({"_id": _to_object_id(emp_id)})
    return {"message": f"Employee '{emp_id}' deleted successfully"}
# Get all employees of a company.
def get_all_employees(company_id: str) -> list:

    docs = list(database.employees_collection.find({"company_id": company_id}))

    for doc in docs:
        doc["emp_id"] = str(doc.pop("_id"))

    return docs


# Get one employee from a company.
def get_employee(company_id: str, emp_id: str) -> dict:

    doc = database.employees_collection.find_one({
        "_id": _to_object_id(emp_id),
        "company_id": company_id
    })

    if not doc:
        raise HTTPException(
            status_code=404,
            detail=f"Employee '{emp_id}' not found in this company"
        )

    doc["emp_id"] = str(doc.pop("_id"))
    return doc