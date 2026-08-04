from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException

from app.config import database
from app.controllers import employee_controller, attendance_controller
from app.models.schemas import GeneratePayrollRequest
from app.services.payroll_calculator import generate_employee_payroll


def _to_object_id(payroll_batch_id: str) -> ObjectId:
    try:
        return ObjectId(payroll_batch_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail=f"'{payroll_batch_id}' is not a valid payroll_batch_id")


def generate_payroll(request: GeneratePayrollRequest) -> dict:

    employees_payroll = []
    skipped_employees = []

    emp_type_value = getattr(request.emp_type, "value", request.emp_type)
    department_value = getattr(request.department, "value", request.department) if request.department else None

    for emp_id in request.employee_ids:
        employee = employee_controller.get_employee_or_none(emp_id)

        if employee is None:
            skipped_employees.append({"emp_id": emp_id, "reason": "Employee not found"})
            continue

        if employee["salary_type"] != emp_type_value:
            skipped_employees.append({
                "emp_id": emp_id,
                "reason": f"Employee salary_type is '{employee['salary_type']}', "
                f"does not match requested emp_type '{emp_type_value}'",
            })
            continue

        if request.company_id and employee["company_id"] != request.company_id:
            skipped_employees.append({
                "emp_id": emp_id,
                "reason": f"Employee belongs to company '{employee['company_id']}', "
                f"does not match requested company_id filter '{request.company_id}'",
            })
            continue

        if department_value and employee["department"] != department_value:
            skipped_employees.append({
                "emp_id": emp_id,
                "reason": f"Employee department is '{employee['department']}', "
                f"does not match requested department filter '{department_value}'",
            })
            continue

        attendance = attendance_controller.get_attendance_summary(
            emp_id, request.pay_period_start, request.pay_period_end
        )

        # No attendance marked at all for this pay period refuse to generate
        # a payslip off zero data rather than producing a near-zero/negative one.
        if attendance["present_days"] == 0:
            skipped_employees.append({
                "emp_id": emp_id,
                "reason": "No attendance records found for this pay period",
            })
            continue

        payroll = generate_employee_payroll(employee, attendance)
        employees_payroll.append(payroll)

    if not employees_payroll:
        raise HTTPException(
            status_code=400,
            detail={"message": "No valid employees to generate payroll for.", "skipped_employees": skipped_employees},
        )

    response = {
        "payroll_type": request.payroll_type,
        "pay_period": {
            "start": str(request.pay_period_start),
            "end": str(request.pay_period_end),
            "label": f"{request.pay_period_start.strftime('%d %b %Y')} - "
            f"{request.pay_period_end.strftime('%d %b %Y')}",
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "employees_payroll": employees_payroll,
        "skipped_employees": skipped_employees or None,
    }

    database.payrolls_collection.insert_one(response)
    response["payroll_batch_id"] = str(response.pop("_id"))
    return response


def get_payroll_batch(payroll_batch_id: str) -> dict:
    doc = database.payrolls_collection.find_one({"_id": _to_object_id(payroll_batch_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Payroll batch not found")
    doc["payroll_batch_id"] = str(doc.pop("_id"))
    return doc