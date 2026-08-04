

from typing import List, Optional

from fastapi import APIRouter, Query

from app.controllers import employee_controller
from app.models.employee_schema import EmployeeCreateRequest, EmployeeUpdateRequest, EmployeeResponse

router = APIRouter(prefix="/api/employees", tags=["Employee"])

 #create a new employee under a company (companyid must already exist).
@router.post("/", response_model=EmployeeResponse)
def create_employee(payload: EmployeeCreateRequest):
    return employee_controller.create_employee(payload)

#list employees
@router.get("/", response_model=List[EmployeeResponse] | EmployeeResponse)
def get_employees(
    company_id: str = Query(..., description="Company ID"),
    emp_id: Optional[str] = Query(None, description="Employee ID"),
):
    return employee_controller.get_employees(company_id, emp_id)

#update an employees fields.
@router.put("/{emp_id}", response_model=EmployeeResponse)
def update_employee(emp_id: str, payload: EmployeeUpdateRequest):
    return employee_controller.update_employee(emp_id, payload)

 #delete an employee.
@router.delete("/{emp_id}")
def delete_employee(emp_id: str):
    return employee_controller.delete_employee(emp_id)
