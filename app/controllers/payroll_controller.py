

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException

from app.data.dummy_employees import get_employee_by_id
from app.models.schemas import GeneratePayrollRequest
from app.services.payroll_calculator import generate_employee_payroll

PAYROLL_BATCHES: dict = {}


def generate_payroll(request: GeneratePayrollRequest) -> dict:

    employees_payroll = []
    skipped_employees = []

    for emp_id in request.employee_ids:
        employee = get_employee_by_id(emp_id)

        if employee is None:
            skipped_employees.append({"emp_id": emp_id, "reason": "Employee not found"})
            continue

        if employee["salary_type"] != request.emp_type:
            skipped_employees.append(
                {
                    "emp_id": emp_id,
                    "reason": f"Employee salary_type is '{employee['salary_type']}', "
                    f"does not match requested emp_type '{request.emp_type}'",
                }
            )
            continue

        if request.department and employee["department"] != request.department:
            skipped_employees.append(
                {
                    "emp_id": emp_id,
                    "reason": f"Employee department is '{employee['department']}', "
                    f"does not match requested department filter '{request.department}'",
                }
            )
            continue

        payroll = generate_employee_payroll(
            employee, request.pay_period_start, request.pay_period_end
        )
        employees_payroll.append(payroll)

    if not employees_payroll:
        raise HTTPException(
            status_code=400,
            detail="No valid employees to generate payroll for. See skipped_employees for reasons.",
        )

    payroll_batch_id = f"PB-{uuid.uuid4().hex[:8].upper()}"

    response = {
        "payroll_batch_id": payroll_batch_id,
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

    PAYROLL_BATCHES[payroll_batch_id] = response
    return response


def get_payroll_batch(payroll_batch_id: str) -> dict:

    batch = PAYROLL_BATCHES.get(payroll_batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Payroll batch not found")
    return batch
