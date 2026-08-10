from fastapi import APIRouter, Depends

from app.core.dependencies import require_company
from app.controllers import payroll_controller
from app.models.schemas import GeneratePayrollRequest, GeneratePayrollResponse

router = APIRouter(prefix="/api/payroll", tags=["Payroll"])


@router.post("/generate", response_model=GeneratePayrollResponse)
def generate_payroll(request: GeneratePayrollRequest, current_user: dict = Depends(require_company)):
    return payroll_controller.generate_payroll(request, current_user["company_id"])


@router.get("/{payroll_batch_id}", response_model=GeneratePayrollResponse)
def get_payroll(payroll_batch_id: str, current_user: dict = Depends(require_company)):
    return payroll_controller.get_payroll_batch(payroll_batch_id, current_user["company_id"])


@router.delete("/{payroll_batch_id}")
def delete_payroll(payroll_batch_id: str, current_user: dict = Depends(require_company)):
    return payroll_controller.delete_payroll_batch(payroll_batch_id, current_user["company_id"])