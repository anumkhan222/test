

from fastapi import APIRouter

from app.controllers import company_settings_controller
from app.models.company_settings_schema import (
    CompanySettingsCreateRequest,
    CompanySettingsUpdateRequest,
    CompanySettingsResponse,
)

router = APIRouter(prefix="/api/companies/{company_id}/settings", tags=["Company Settings"])


@router.post("/", response_model=CompanySettingsResponse)
def create_settings(company_id: str, payload: CompanySettingsCreateRequest):
    #Create payroll settings for a company (fails if the company doesn't exist or already has settings).
    return company_settings_controller.create_settings(company_id, payload)


@router.get("/", response_model=CompanySettingsResponse)
def get_settings(company_id: str):
    #Get a company's payroll settings.
    return company_settings_controller.get_settings(company_id)


@router.put("/", response_model=CompanySettingsResponse)
def update_settings(company_id: str, payload: CompanySettingsUpdateRequest):
    #Update a company's payroll settings.
    return company_settings_controller.update_settings(company_id, payload)


@router.delete("/")
def delete_settings(company_id: str):
    #Delete a company's payroll settings.
    return company_settings_controller.delete_settings(company_id)
