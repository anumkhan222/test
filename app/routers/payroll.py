from fastapi import APIRouter

from app.controllers import payroll_controller
from app.models.schemas import GeneratePayrollRequest, GeneratePayrollResponse

router = APIRouter(prefix="/api/payroll", tags=["Payroll"])


@router.post("/generate", response_model=GeneratePayrollResponse)
def generate_payroll(request: GeneratePayrollRequest):
    #Generate a payroll batch for the given employees and pay period.
    return payroll_controller.generate_payroll(request)


@router.get("/{payroll_batch_id}")
def get_payroll_batch(payroll_batch_id: str):
    #Fetch a previously generated payroll batch by its ID.
    return payroll_controller.get_payroll_batch(payroll_batch_id)
