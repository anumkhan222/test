from typing import List, Optional, Union
from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, require_company
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


# Create a new company profile — links it to the logged-in user as owner
@router.post("/", response_model=CompanyResponse)
def create_company(payload: CompanyCreateRequest, current_user: dict = Depends(get_current_user)):
    return company_controller.create_company(payload, current_user["user_id"])


# Get the logged-in user's own company (no more list-all — that leaked every company to every user)
@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: str, current_user: dict = Depends(require_company)):
    company_controller.ensure_owns_company(current_user, company_id)
    return company_controller.get_company(company_id)


# Update a company's profile fields
@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: str, payload: CompanyUpdateRequest, current_user: dict = Depends(require_company)):
    company_controller.ensure_owns_company(current_user, company_id)
    return company_controller.update_company(company_id, payload)


# Delete a company profile (and its settings, if any)
@router.delete("/{company_id}")
def delete_company(company_id: str, current_user: dict = Depends(require_company)):
    company_controller.ensure_owns_company(current_user, company_id)
    return company_controller.delete_company(company_id)


# Create payroll settings for a company
@router.post("/{company_id}/settings/", response_model=CompanySettingsResponse)
def create_settings(company_id: str, payload: CompanySettingsCreateRequest, current_user: dict = Depends(require_company)):
    company_controller.ensure_owns_company(current_user, company_id)
    return company_controller.create_settings(company_id, payload)


# Get a company's payroll settings
@router.get("/{company_id}/settings/", response_model=CompanySettingsResponse)
def get_settings(company_id: str, current_user: dict = Depends(require_company)):
    company_controller.ensure_owns_company(current_user, company_id)
    return company_controller.get_settings(company_id)


# Update a company's payroll settings
@router.put("/{company_id}/settings/", response_model=CompanySettingsResponse)
def update_settings(company_id: str, payload: CompanySettingsUpdateRequest, current_user: dict = Depends(require_company)):
    company_controller.ensure_owns_company(current_user, company_id)
    return company_controller.update_settings(company_id, payload)


# Delete a company's payroll settings
@router.delete("/{company_id}/settings/")
def delete_settings(company_id: str, current_user: dict = Depends(require_company)):
    company_controller.ensure_owns_company(current_user, company_id)
    return company_controller.delete_settings(company_id)