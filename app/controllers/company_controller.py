import uuid
from datetime import datetime, timezone
from typing import  Optional
from fastapi import HTTPException

from app.config import database
from app.models.company_schema import CompanyCreateRequest, CompanyUpdateRequest


def _generate_company_id() -> str:

    return f"COMP-{uuid.uuid4().hex[:8].upper()}"


def create_company(payload: CompanyCreateRequest) -> dict:

    company_id = _generate_company_id()
    now = datetime.now(timezone.utc).isoformat()

    company_doc = payload.model_dump(mode="json")
    company_doc["company_id"] = company_id
    company_doc["created_at"] = now
    company_doc["updated_at"] = now

    database.companies_collection.insert_one(company_doc)
    company_doc.pop("_id", None)
    return company_doc


def get_companies(company_id: Optional[str] = None):
    # If company_id is provided, return one company
    if company_id:
        doc = database.companies_collection.find_one(
            {"company_id": company_id},
            {"_id": 0}
        )

        if not doc:
            raise HTTPException(
                status_code=404,
                detail=f"Company '{company_id}' not found"
            )
        return doc

    return list(database.companies_collection.find({}, {"_id": 0}))

def update_company(company_id: str, payload: CompanyUpdateRequest) -> dict:

    get_company(company_id)  

    update_fields = {
        k: v for k, v in payload.model_dump(exclude_unset=True, mode="json").items() if v is not None
    }
    update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()

    database.companies_collection.update_one({"company_id": company_id}, {"$set": update_fields})
    return get_company(company_id)


def delete_company(company_id: str) -> dict:

    get_company(company_id)  
    database.companies_collection.delete_one({"company_id": company_id})
    database.company_settings_collection.delete_one({"company_id": company_id})
    return {"message": f"Company '{company_id}' (and its settings, if any) deleted successfully"}
