
from datetime import datetime, timezone

from fastapi import HTTPException

from app.config import database
from app.controllers import company_controller
from app.models.company_settings_schema import CompanySettingsCreateRequest, CompanySettingsUpdateRequest


def create_settings(company_id: str, payload: CompanySettingsCreateRequest) -> dict:

    company_controller.get_company(company_id)  

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


def get_settings(company_id: str) -> dict:

    doc = database.company_settings_collection.find_one({"company_id": company_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail=f"No settings found for company '{company_id}'")
    return doc


def update_settings(company_id: str, payload: CompanySettingsUpdateRequest) -> dict:

    get_settings(company_id)  

    update_fields = {
        k: v for k, v in payload.model_dump(exclude_unset=True, mode="json").items() if v is not None
    }
    update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()

    database.company_settings_collection.update_one({"company_id": company_id}, {"$set": update_fields})
    return get_settings(company_id)


def delete_settings(company_id: str) -> dict:

    get_settings(company_id)  
    database.company_settings_collection.delete_one({"company_id": company_id})
    return {"message": f"Settings for company '{company_id}' deleted successfully"}
