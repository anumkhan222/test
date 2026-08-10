from fastapi import FastAPI

from app.routers import payroll, company,employee,attendance,auth
app = FastAPI(
    title="Payroll Payload Generation API",
    description="Generates payroll payloads for employees based on "
    "dummy data and a Salary -> Allowances -> Deductions calculation "
    "pipeline.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(company.router)
app.include_router(employee.router)
app.include_router(attendance.router)
app.include_router(payroll.router)


@app.get("/")
def root():
    return {"message": "Payroll Payload Generation API is running. "}
