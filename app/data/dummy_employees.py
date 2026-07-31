"""
Dummy employee data.
This file is the single source for employee records — there is no
database. Each employee has:
  - basic profile info (name, email, department, etc.)
  - a salary_rule (base pay + the attendance_policy used to judge attendance)
  - deduction_rules (list of deductions applied to them)
  - allowance_rules (list of allowances applied to them)
  - attendance_events: RAW clock-in/clock-out style events (leave dates,
    absent dates, late clock-ins, overtime clock-outs) for June 2026.
"""

EMPLOYEES = [
    {
        "emp_id": "EMP001",
        "emp_name": "Dianne Russell",
        "email": "diannerussell@gmail.com",
        "profile_image": "https://i.pravatar.cc/150?img=1",
        "department": "UI/UX",
        "designation": "UI/UX Designer",
        "salary_type": "Monthly",
        "salary_rule": {
            "base_salary": 25000,
            "pay_period": "Monthly",
            "payment_method": "Bank Transfer",
            "currency": "USD",
            "include_allowance_and_overtime_in_payroll": True,
            "attendance_policy": {
                "standard_working_days_per_month": 22,
                "standard_hours_per_day": 8,
                "standard_clock_in": "09:00",
                "standard_clock_out": "18:00",
                "paid_leaves_allowed_per_month": 2,
            },
        },
        "deduction_rules": [
            {"deduction_type": "UIF", "amount_type": "Fixed", "amount": 20},
            {"deduction_type": "Income Tax", "amount_type": "Percentage", "amount": 5},
        ],
        "allowance_rules": [
            {"allowance_type": "Pick and Drop", "amount_type": "Fixed", "amount": 56},
        ],
        "attendance_events": {
            "leave_dates": ["2026-06-15", "2026-06-22"],
            "absent_dates": [],
            "late_clock_ins": {"2026-06-03": "09:35"},
            "overtime_clock_outs": {"2026-06-02": "20:00", "2026-06-04": "19:30"},
        },
    },
    {
        "emp_id": "EMP002",
        "emp_name": "Robert Fox",
        "email": "robertfox@gmail.com",
        "profile_image": "https://i.pravatar.cc/150?img=2",
        "department": "Frontend",
        "designation": "Frontend Developer",
        "salary_type": "Monthly",
        "salary_rule": {
            "base_salary": 30000,
            "pay_period": "Monthly",
            "payment_method": "Bank Transfer",
            "currency": "USD",
            "include_allowance_and_overtime_in_payroll": True,
            "attendance_policy": {
                "standard_working_days_per_month": 22,
                "standard_hours_per_day": 8,
                "standard_clock_in": "09:00",
                "standard_clock_out": "18:00",
                "paid_leaves_allowed_per_month": 2,
            },
        },
        "deduction_rules": [
            {"deduction_type": "UIF", "amount_type": "Fixed", "amount": 25},
        ],
        "allowance_rules": [
            {"allowance_type": "Expenses", "amount_type": "Fixed", "amount": 40},
        ],
        "attendance_events": {
            "leave_dates": [],
            "absent_dates": [],
            "late_clock_ins": {},
            "overtime_clock_outs": {"2026-06-01": "19:00", "2026-06-08": "19:00"},
        },
    },
    {
        "emp_id": "EMP003",
        "emp_name": "Jane Cooper",
        "email": "janecooper@gmail.com",
        "profile_image": "https://i.pravatar.cc/150?img=3",
        "department": "Backend",
        "designation": "Backend Developer",
        "salary_type": "Monthly",
        "salary_rule": {
            "base_salary": 32000,
            "pay_period": "Monthly",
            "payment_method": "Bank Transfer",
            "currency": "USD",
            "include_allowance_and_overtime_in_payroll": True,
            "attendance_policy": {
                "standard_working_days_per_month": 22,
                "standard_hours_per_day": 8,
                "standard_clock_in": "09:00",
                "standard_clock_out": "18:00",
                "paid_leaves_allowed_per_month": 2,
            },
        },
        "deduction_rules": [
            {"deduction_type": "Income Tax", "amount_type": "Percentage", "amount": 6},
        ],
        "allowance_rules": [],
        "attendance_events": {
            "leave_dates": ["2026-06-16", "2026-06-17", "2026-06-18"],
            "absent_dates": [],
            "late_clock_ins": {"2026-06-01": "09:20", "2026-06-02": "09:15"},
            "overtime_clock_outs": {},
        },
    },
    {
        "emp_id": "EMP004",
        "emp_name": "Courtney Henry",
        "email": "courtneyhenry@gmail.com",
        "profile_image": "https://i.pravatar.cc/150?img=4",
        "department": "UI/UX",
        "designation": "Product Designer",
        "salary_type": "Hourly",
        "salary_rule": {
            "base_salary": 25,
            "pay_period": "Weekly",
            "payment_method": "Bank Transfer",
            "currency": "USD",
            "include_allowance_and_overtime_in_payroll": True,
            "attendance_policy": {
                "standard_working_days_per_month": 22,
                "standard_hours_per_day": 8,
                "standard_clock_in": "09:00",
                "standard_clock_out": "17:00",
                "paid_leaves_allowed_per_month": 1,
            },
        },
        "deduction_rules": [
            {"deduction_type": "UIF", "amount_type": "Fixed", "amount": 10},
        ],
        "allowance_rules": [
            {"allowance_type": "Pick and Drop", "amount_type": "Fixed", "amount": 15},
        ],
        "attendance_events": {
            "leave_dates": [],
            "absent_dates": [],
            "late_clock_ins": {},
            "overtime_clock_outs": {"2026-06-03": "19:00"},
        },
    },
    {
        "emp_id": "EMP005",
        "emp_name": "Devon Lane",
        "email": "devonlane@gmail.com",
        "profile_image": "https://i.pravatar.cc/150?img=5",
        "department": "Backend",
        "designation": "Backend Lead",
        "salary_type": "Monthly",
        "salary_rule": {
            "base_salary": 45000,
            "pay_period": "Monthly",
            "payment_method": "Bank Transfer",
            "currency": "USD",
            "include_allowance_and_overtime_in_payroll": True,
            "attendance_policy": {
                "standard_working_days_per_month": 22,
                "standard_hours_per_day": 8,
                "standard_clock_in": "09:00",
                "standard_clock_out": "18:00",
                "paid_leaves_allowed_per_month": 3,
            },
        },
        "deduction_rules": [
            {"deduction_type": "UIF", "amount_type": "Fixed", "amount": 30},
            {"deduction_type": "Income Tax", "amount_type": "Percentage", "amount": 8},
        ],
        "allowance_rules": [
            {"allowance_type": "Expenses", "amount_type": "Percentage", "amount": 2},
        ],
        "attendance_events": {
            "leave_dates": ["2026-06-19"],
            "absent_dates": [],
            "late_clock_ins": {},
            "overtime_clock_outs": {"2026-06-04": "19:15", "2026-06-05": "19:30"},
        },
    },
    {
        "emp_id": "EMP006",
        "emp_name": "Esther Howard",
        "email": "estherhoward@gmail.com",
        "profile_image": "https://i.pravatar.cc/150?img=6",
        "department": "Frontend",
        "designation": "Frontend Lead",
        "salary_type": "Monthly",
        "salary_rule": {
            "base_salary": 40000,
            "pay_period": "Monthly",
            "payment_method": "Bank Transfer",
            "currency": "USD",
            "include_allowance_and_overtime_in_payroll": True,
            "attendance_policy": {
                "standard_working_days_per_month": 22,
                "standard_hours_per_day": 8,
                "standard_clock_in": "09:00",
                "standard_clock_out": "18:00",
                "paid_leaves_allowed_per_month": 2,
            },
        },
        "deduction_rules": [
            {"deduction_type": "UIF", "amount_type": "Fixed", "amount": 28},
        ],
        "allowance_rules": [
            {"allowance_type": "Pick and Drop", "amount_type": "Fixed", "amount": 50},
        ],
        "attendance_events": {
            "leave_dates": [],
            "absent_dates": [],
            "late_clock_ins": {"2026-06-05": "09:40"},
            "overtime_clock_outs": {"2026-06-01": "19:00", "2026-06-02": "19:00", "2026-06-09": "19:00"},
        },
    },
    {
        "emp_id": "EMP007",
        "emp_name": "Cameron Williamson",
        "email": "cameronwilliamson@gmail.com",
        "profile_image": "https://i.pravatar.cc/150?img=7",
        "department": "Backend",
        "designation": "Backend Developer",
        "salary_type": "Hourly",
        "salary_rule": {
            "base_salary": 22,
            "pay_period": "Weekly",
            "payment_method": "Bank Transfer",
            "currency": "USD",
            "include_allowance_and_overtime_in_payroll": False,
            "attendance_policy": {
                "standard_working_days_per_month": 22,
                "standard_hours_per_day": 8,
                "standard_clock_in": "09:00",
                "standard_clock_out": "17:00",
                "paid_leaves_allowed_per_month": 1,
            },
        },
        "deduction_rules": [
            {"deduction_type": "UIF", "amount_type": "Fixed", "amount": 8},
        ],
        "allowance_rules": [
            {"allowance_type": "Expenses", "amount_type": "Fixed", "amount": 20},
        ],
        "attendance_events": {
            "leave_dates": ["2026-06-05"],
            "absent_dates": [],
            "late_clock_ins": {"2026-06-04": "09:45"},
            "overtime_clock_outs": {},
        },
    },
    {
        "emp_id": "EMP008",
        "emp_name": "Brooklyn Simmons",
        "email": "brooklynsimmons@gmail.com",
        "profile_image": "https://i.pravatar.cc/150?img=8",
        "department": "UI/UX",
        "designation": "UI/UX Designer",
        "salary_type": "Monthly",
        "salary_rule": {
            "base_salary": 27000,
            "pay_period": "Monthly",
            "payment_method": "Bank Transfer",
            "currency": "USD",
            "include_allowance_and_overtime_in_payroll": True,
            "attendance_policy": {
                "standard_working_days_per_month": 22,
                "standard_hours_per_day": 8,
                "standard_clock_in": "09:00",
                "standard_clock_out": "18:00",
                "paid_leaves_allowed_per_month": 2,
            },
        },
        "deduction_rules": [
            {"deduction_type": "Income Tax", "amount_type": "Percentage", "amount": 5},
        ],
        "allowance_rules": [
            {"allowance_type": "Pick and Drop", "amount_type": "Fixed", "amount": 30},
        ],
        "attendance_events": {
            "leave_dates": ["2026-06-23", "2026-06-24"],
            "absent_dates": [],
            "late_clock_ins": {},
            "overtime_clock_outs": {"2026-06-03": "19:00"},
        },
    },
    {
        "emp_id": "EMP009",
        "emp_name": "Kristin Watson",
        "email": "kristinwatson@gmail.com",
        "profile_image": "https://i.pravatar.cc/150?img=9",
        "department": "Frontend",
        "designation": "Frontend Developer",
        "salary_type": "Monthly",
        "salary_rule": {
            "base_salary": 28000,
            "pay_period": "Monthly",
            "payment_method": "Bank Transfer",
            "currency": "USD",
            "include_allowance_and_overtime_in_payroll": True,
            "attendance_policy": {
                "standard_working_days_per_month": 22,
                "standard_hours_per_day": 8,
                "standard_clock_in": "09:00",
                "standard_clock_out": "18:00",
                "paid_leaves_allowed_per_month": 2,
            },
        },
        "deduction_rules": [
            {"deduction_type": "UIF", "amount_type": "Fixed", "amount": 22},
        ],
        "allowance_rules": [],
        "attendance_events": {
            "leave_dates": ["2026-06-08", "2026-06-09"],
            "absent_dates": ["2026-06-25", "2026-06-26"],
            "late_clock_ins": {"2026-06-01": "09:50", "2026-06-02": "09:30", "2026-06-03": "09:45"},
            "overtime_clock_outs": {},
        },
    },
    {
        "emp_id": "EMP010",
        "emp_name": "Guy Hawkins",
        "email": "guyhawkins@gmail.com",
        "profile_image": "https://i.pravatar.cc/150?img=10",
        "department": "Backend",
        "designation": "Backend Developer",
        "salary_type": "Monthly",
        "salary_rule": {
            "base_salary": 31000,
            "pay_period": "Monthly",
            "payment_method": "Bank Transfer",
            "currency": "USD",
            "include_allowance_and_overtime_in_payroll": True,
            "attendance_policy": {
                "standard_working_days_per_month": 22,
                "standard_hours_per_day": 8,
                "standard_clock_in": "09:00",
                "standard_clock_out": "18:00",
                "paid_leaves_allowed_per_month": 2,
            },
        },
        "deduction_rules": [
            {"deduction_type": "UIF", "amount_type": "Fixed", "amount": 24},
            {"deduction_type": "Income Tax", "amount_type": "Percentage", "amount": 5},
        ],
        "allowance_rules": [
            {"allowance_type": "Expenses", "amount_type": "Fixed", "amount": 35},
        ],
        "attendance_events": {
            "leave_dates": [],
            "absent_dates": [],
            "late_clock_ins": {},
            "overtime_clock_outs": {"2026-06-01": "20:00", "2026-06-02": "20:00", "2026-06-03": "20:00"},
        },
    },
]
def get_employee_by_id(emp_id: str):   
    #get single employee dictionary by their emp id.
    #The API only receives employee ids in the request this is how we turn an id like "EMP001" into the full employee record
    for emp in EMPLOYEES:
        if emp["emp_id"] == emp_id:
            return emp
    return None

def get_all_employees():
    return EMPLOYEES
