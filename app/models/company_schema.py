from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from app.models.enums import BusinessType, BusinessSize, PayrollCycle


#store company social media handles
class SocialLinks(BaseModel):
    twitter: Optional[str] = Field(None, description="Handle only, e.g. 'Leadsoftwares8789' (twitter.com/<this>)")
    facebook: Optional[str] = Field(None, description="Handle only, e.g. 'Leadsoftwares8789' (facebook.com/<this>)")
    linkedin: Optional[str] = Field(None, description="Handle only, e.g. 'Leadsoftwares8789' (linkedin.com/company/<this>)")


#request model to create a new company
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


#request model to update company details
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


#response model for company details
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


#request model to create company settings
class CompanySettingsCreateRequest(BaseModel):
    salary_payment_day: int = Field(
        ..., ge=1, le=31, description="Day of the month salaries are paid, e.g. 28"
    )
    allow_overtime: bool = Field(True, description="Whether this company pays overtime at all")
    overtime_rate_multiplier: float = Field(1.5, description="Overtime pay multiplier, e.g. 1.5x hourly rate")
    standard_working_days_per_week: int = Field(5, description="e.g. 5 for Mon-Fri, 6 if Saturdays are working days")
    standard_working_hours_per_day: float = Field(8, description="Standard shift length in hours")
    standard_clock_in: str = Field("09:00", description="Default expected clock-in time, 24hr HH:MM")
    standard_clock_out: str = Field("18:00", description="Default expected clock-out time, 24hr HH:MM")
    weekend_days: List[str] = Field(
        default_factory=lambda: ["Saturday", "Sunday"],
        description="Days of the week not counted as working days",
    )
    paid_leaves_allowed_per_month: int = Field(2, description="Default paid leave allowance per employee per month")
    late_arrival_grace_minutes: int = Field(
        0, description="Grace period in minutes before a clock-in is considered late"
    )
    default_payroll_cycle: PayrollCycle = Field(
        PayrollCycle.MONTHLY,
        description="Default payroll cycle"
    )


#request model to update company settings
class CompanySettingsUpdateRequest(BaseModel):
    salary_payment_day: Optional[int] = Field(None, ge=1, le=31)
    allow_overtime: Optional[bool] = None
    overtime_rate_multiplier: Optional[float] = None
    standard_working_days_per_week: Optional[int] = None
    standard_working_hours_per_day: Optional[float] = None
    standard_clock_in: Optional[str] = None
    standard_clock_out: Optional[str] = None
    weekend_days: Optional[List[str]] = None
    paid_leaves_allowed_per_month: Optional[int] = None
    late_arrival_grace_minutes: Optional[int] = None
    default_payroll_cycle: Optional[PayrollCycle] = None


#response model for company settings
class CompanySettingsResponse(BaseModel):
    company_id: str
    salary_payment_day: int
    allow_overtime: bool
    overtime_rate_multiplier: float
    standard_working_days_per_week: int
    standard_working_hours_per_day: float
    standard_clock_in: str
    standard_clock_out: str
    weekend_days: List[str]
    paid_leaves_allowed_per_month: int
    late_arrival_grace_minutes: int
    default_payroll_cycle: PayrollCycle
    created_at: str
    updated_at: str