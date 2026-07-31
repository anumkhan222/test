from fastapi import FastAPI

from app.routers import payroll, company,company_settings
app = FastAPI(
    title="Payroll Payload Generation API",
    description="Generates payroll payloads for employees based on "
    "dummy data and a Salary -> Allowances -> Deductions calculation "
    "pipeline.",
    version="1.0.0",
)

app.include_router(company.router)
#hgjhkgjhg
app.include_router(company_settings.router)
app.include_router(payroll.router)


@app.get("/")
def root():
    return {"message": "Payroll Payload Generation API is running. "}
