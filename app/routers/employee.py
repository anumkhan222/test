from typing import List, Optional
from fastapi import APIRouter, Depends, Query

from app.core.dependencies import require_company
from app.controllers import employee_controller
from app.models.employee_schema import EmployeeCreateRequest, EmployeeUpdateRequest, EmployeeResponse

router = APIRouter(prefix="/api/employees", tags=["Employee"])


@router.post("/", response_model=EmployeeResponse)
def create_employee(payload: EmployeeCreateRequest, current_user: dict = Depends(require_company)):
    return employee_controller.create_employee(payload, current_user["company_id"])


@router.get("/", response_model=List[EmployeeResponse] | EmployeeResponse)
def get_employees(
    emp_id: Optional[str] = Query(None, description="Employee ID"),
    department: Optional[str] = Query(None, description="Department"),
    salary_type: Optional[str] = Query(None, description="Salary Type"),
    pay_period: Optional[str] = Query(None, description="Pay Period"),
    current_user: dict = Depends(require_company),
):
    return employee_controller.get_employees(
        company_id=current_user["company_id"],
        emp_id=emp_id,
        department=department,
        salary_type=salary_type,
        pay_period=pay_period,
    )

@router.put("/{emp_id}", response_model=EmployeeResponse)
def update_employee(emp_id: str, payload: EmployeeUpdateRequest, current_user: dict = Depends(require_company)):
    return employee_controller.update_employee(emp_id, payload, current_user["company_id"])


@router.delete("/{emp_id}")
def delete_employee(emp_id: str, current_user: dict = Depends(require_company)):
    return employee_controller.delete_employee(emp_id, current_user["company_id"])