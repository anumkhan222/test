from typing import List, Optional, Union

from fastapi import APIRouter

from app.controllers import company_controller
from app.models.company_schema import CompanyCreateRequest, CompanyUpdateRequest, CompanyResponse

router = APIRouter(prefix="/api/companies", tags=["Company"])


@router.post("/", response_model=CompanyResponse)
def create_company(payload: CompanyCreateRequest):
    #Create a new company profile.
    return company_controller.create_company(payload)


@router.get("/", response_model=Union[CompanyResponse, List[CompanyResponse]])
def get_companies(company_id: Optional[str] = None):
    #Get all companies or a single company by company_id.
    return company_controller.get_companies(company_id)

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: str, payload: CompanyUpdateRequest):
    #Update a company's profile fields.
    return company_controller.update_company(company_id, payload)


@router.delete("/{company_id}")
def delete_company(company_id: str):
    #Delete a company profile (and its settings, if any).
    return company_controller.delete_company(company_id)
