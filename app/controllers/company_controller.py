from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from typing import Optional, Union
from app.config import database
from app.models.company_schema import (
    CompanyCreateRequest,
    CompanyUpdateRequest,
    CompanySettingsCreateRequest,
    CompanySettingsUpdateRequest,
)

#convert a company id string into a MongoDB ObjectId
def _to_object_id(company_id: str) -> ObjectId:
    try:
        return ObjectId(company_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail=f"'{company_id}' is not a valid company_id")

#create a new company and save it in the database
def create_company(payload: CompanyCreateRequest) -> dict:

    now = datetime.now(timezone.utc).isoformat()

    company_doc = payload.model_dump(mode="json")
    company_doc["created_at"] = now
    company_doc["updated_at"] = now

    database.companies_collection.insert_one(company_doc)  # fills in company_doc["_id"]

    company_doc["company_id"] = str(company_doc.pop("_id"))
    return company_doc

#get one company or all companies from the database
def get_company(company_id: Optional[str] = None):

    if company_id:
        doc = database.companies_collection.find_one(
            {"_id": _to_object_id(company_id)}
        )

        if not doc:
            raise HTTPException(
                status_code=404,
                detail=f"Company '{company_id}' not found",
            )

        doc["company_id"] = str(doc.pop("_id"))
        return doc

    docs = list(database.companies_collection.find({}))
    for doc in docs:
        doc["company_id"] = str(doc.pop("_id"))
    return docs

#update an existing companys details
def update_company(company_id: str, payload: CompanyUpdateRequest) -> dict:

    get_company(company_id)  

    update_fields = {}
    if payload.logo_url is not None:
        update_fields["logo_url"] = payload.logo_url
    if payload.business_name is not None:
        update_fields["business_name"] = payload.business_name
    if payload.business_type is not None:
        update_fields["business_type"] = payload.business_type.value
    if payload.business_size is not None:
        update_fields["business_size"] = payload.business_size.value
    if payload.about is not None:
        update_fields["about"] = payload.about
    if payload.business_email is not None:
        update_fields["business_email"] = payload.business_email
    if payload.phone_country_code is not None:
        update_fields["phone_country_code"] = payload.phone_country_code
    if payload.phone_number is not None:
        update_fields["phone_number"] = payload.phone_number
    if payload.business_url is not None:
        update_fields["business_url"] = payload.business_url
    if payload.social_links is not None:
        update_fields["social_links"] = payload.social_links.model_dump()

    update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()

    database.companies_collection.update_one({"_id": _to_object_id(company_id)}, {"$set": update_fields})
    return get_company(company_id)

#delete a company and its settings
def delete_company(company_id: str) -> dict:
    get_company(company_id)  
    database.companies_collection.delete_one({"_id": _to_object_id(company_id)})
    database.company_settings_collection.delete_one({"company_id": company_id})
    return {"message": f"Company '{company_id}' (and its settings, if any) deleted successfully"}


#create settings for a company
def create_settings(company_id: str, payload: CompanySettingsCreateRequest) -> dict:

    get_company(company_id)  

    existing = database.company_settings_collection.find_one({"company_id": company_id})
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Settings already exist for company '{company_id}'. Use PUT to update them.",
        )

    now = datetime.now(timezone.utc).isoformat()
    settings_doc = payload.model_dump(mode="json")
    settings_doc["company_id"] = company_id
    settings_doc["created_at"] = now
    settings_doc["updated_at"] = now

    database.company_settings_collection.insert_one(settings_doc)
    settings_doc.pop("_id", None)
    return settings_doc

#get the settings of a company
def get_settings(company_id: str) -> dict:

    doc = database.company_settings_collection.find_one({"company_id": company_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail=f"No settings found for company '{company_id}'")
    return doc

#update the settings of a company
def update_settings(company_id: str, payload: CompanySettingsUpdateRequest) -> dict:

    get_settings(company_id)  

    update_fields = {}
    if payload.salary_payment_day is not None:
        update_fields["salary_payment_day"] = payload.salary_payment_day
    if payload.allow_overtime is not None:
        update_fields["allow_overtime"] = payload.allow_overtime
    if payload.overtime_rate_multiplier is not None:
        update_fields["overtime_rate_multiplier"] = payload.overtime_rate_multiplier
    if payload.standard_working_days_per_week is not None:
        update_fields["standard_working_days_per_week"] = payload.standard_working_days_per_week
    if payload.standard_working_hours_per_day is not None:
        update_fields["standard_working_hours_per_day"] = payload.standard_working_hours_per_day
    if payload.standard_clock_in is not None:
        update_fields["standard_clock_in"] = payload.standard_clock_in
    if payload.standard_clock_out is not None:
        update_fields["standard_clock_out"] = payload.standard_clock_out
    if payload.weekend_days is not None:
        update_fields["weekend_days"] = payload.weekend_days
    if payload.paid_leaves_allowed_per_month is not None:
        update_fields["paid_leaves_allowed_per_month"] = payload.paid_leaves_allowed_per_month
    if payload.late_arrival_grace_minutes is not None:
        update_fields["late_arrival_grace_minutes"] = payload.late_arrival_grace_minutes
    if payload.default_payroll_cycle is not None:
        update_fields["default_payroll_cycle"] = payload.default_payroll_cycle.value

    update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()

    database.company_settings_collection.update_one({"company_id": company_id}, {"$set": update_fields})
    return get_settings(company_id)

#delete a company's settings
def delete_settings(company_id: str) -> dict:

    get_settings(company_id)  # raises 404 if settings don't exist
    database.company_settings_collection.delete_one({"company_id": company_id})
    return {"message": f"Settings for company '{company_id}' deleted successfully"}
