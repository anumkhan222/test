from typing import List,Optional,Union
from fastapi import APIRouter

from app.controllers import company_controller
from app.models.company_schema import (
    CompanyCreateRequest,
    CompanyUpdateRequest,
    CompanyResponse,
    CompanySettingsCreateRequest,
    CompanySettingsUpdateRequest,
    CompanySettingsResponse,
)

router = APIRouter(prefix="/api/companies", tags=["Company"])


#Create a new company profile
@router.post("/", response_model=CompanyResponse)
def create_company(payload: CompanyCreateRequest):
    return company_controller.create_company(payload)

#get all compamy or one company
@router.get("/",response_model=Union[List[CompanyResponse], CompanyResponse],
)
def get_company(company_id: Optional[str] = None):
    return company_controller.get_company(company_id)

 #Update a companys profile fields
@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: str, payload: CompanyUpdateRequest):
    return company_controller.update_company(company_id, payload)

#delete a company profile (and its settings, if any)
@router.delete("/{company_id}")
def delete_company(company_id: str):
    return company_controller.delete_company(company_id)

#create payroll settings for a company (fails if the company doesn't exist or already has settings)
@router.post("/{company_id}/settings/", response_model=CompanySettingsResponse)
def create_settings(company_id: str, payload: CompanySettingsCreateRequest):
    return company_controller.create_settings(company_id, payload)

#get a companys payroll settings.
@router.get("/{company_id}/settings/", response_model=CompanySettingsResponse)
def get_settings(company_id: str):
    return company_controller.get_settings(company_id)

#update a companys payroll settings
@router.put("/{company_id}/settings/", response_model=CompanySettingsResponse)
def update_settings(company_id: str, payload: CompanySettingsUpdateRequest):
    return company_controller.update_settings(company_id, payload)

 #delete a companys payroll settings
@router.delete("/{company_id}/settings/")
def delete_settings(company_id: str):
    return company_controller.delete_settings(company_id)
