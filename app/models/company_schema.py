from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl

from app.models.enums import BusinessType, BusinessSize


class SocialLinks(BaseModel):

    twitter: Optional[str] = Field(None, description="Handle only, e.g. 'Leadsoftwares8789' (twitter.com/<this>)")
    facebook: Optional[str] = Field(None, description="Handle only, e.g. 'Leadsoftwares8789' (facebook.com/<this>)")
    linkedin: Optional[str] = Field(None, description="Handle only, e.g. 'Leadsoftwares8789' (linkedin.com/company/<this>)")


class CompanyCreateRequest(BaseModel):
    logo_url: Optional[str] = Field(None, description="URL to the uploaded logo image")
    business_name: str = Field(..., min_length=1, description="The company's display name")
    business_type: BusinessType = Field(..., description="Industry/category, e.g. Information Technology")
    business_size: BusinessSize = Field(..., description="Employee-count bracket, e.g. '1-50 employees'")
    about: Optional[str] = Field(None, description="A short description of the company")
    business_email: EmailStr = Field(..., description="Primary business contact email")
    phone_country_code: str = Field(..., description="Phone country calling code, e.g. '+1'")
    phone_number: str = Field(..., description="Phone number without the country code")
    business_url: Optional[str] = Field(None, description="Company website, e.g. 'leadsoftware.com'")
    social_links: SocialLinks = Field(default_factory=SocialLinks, description="Social media handles")


class CompanyUpdateRequest(BaseModel):
    
    logo_url: Optional[str] = None
    business_name: Optional[str] = None
    business_type: Optional[BusinessType] = None
    business_size: Optional[BusinessSize] = None
    about: Optional[str] = None
    business_email: Optional[EmailStr] = None
    phone_country_code: Optional[str] = None
    phone_number: Optional[str] = None
    business_url: Optional[str] = None
    social_links: Optional[SocialLinks] = None


class CompanyResponse(BaseModel):
    company_id: str
    logo_url: Optional[str] = None
    business_name: str
    business_type: BusinessType
    business_size: BusinessSize
    about: Optional[str] = None
    business_email: EmailStr
    phone_country_code: str
    phone_number: str
    business_url: Optional[str] = None
    social_links: SocialLinks
    created_at: str
    updated_at: str
