from datetime import date

# calculate fixed or percentage amount
def _calc_rule_amount(amount_type: str, amount: float, base: float):
    if amount_type == "Percentage":
        return round((amount / 100) * base, 2)
    return round(amount, 2)

# calculate employee salary based on attendance
def generate_salary(employee: dict, attendance: dict):

    # get salary rules from employee data.
    rule = employee["salary_rule"]
    policy = rule

    base_salary = rule["base_salary"]
    present_days = attendance["present_days"]
    overtime_hours = attendance["overtime_hours"]
    hours_per_day = policy["standard_hours_per_day"]

    # getstandard working days for salary calculation.
    reference_working_days = (
        policy.get("standard_working_days_per_month")
        or attendance["working_days"]
        or 1
    )

    # calculate salary for hourly employees.
    if employee["salary_type"] == "Hourly":
        hourly_rate = base_salary
        basic_salary = round(hourly_rate * hours_per_day * present_days, 2)
        per_day_rate = round(hourly_rate * hours_per_day, 2)

    # calculate salary for monthly employees
    else:
        per_day_rate = (
            round(base_salary / reference_working_days, 2)
            if reference_working_days else 0
        )
        hourly_rate = (
            round(per_day_rate / hours_per_day, 2)
            if hours_per_day else 0
        )
        basic_salary = round(per_day_rate * present_days, 2)

    # calculate overtime pay.
    overtime_rate = round(hourly_rate * 1.5, 2)
    overtime_pay = round(overtime_rate * overtime_hours, 2)

    return basic_salary, overtime_pay, per_day_rate, hourly_rate


# calculate allowances.
def generate_allowances(employee: dict, gross_salary: float):

    line_items = []

    for rule in employee.get("allowance_rules", []):

        amount = _calc_rule_amount(
            rule["amount_type"],
            rule["amount"],
            gross_salary,
        )

        line_items.append(
            {
                "component": rule["allowance_type"],
                "type": "Earnings",
                "amount": amount,
            }
        )

    return line_items


# calcluate attendance related deduction.
def generate_attendance_deductions(
    employee: dict,
    attendance: dict,
    per_day_rate: float,
    hourly_rate: float,
):

    policy = employee["salary_rule"]

    # calculate paid leaves for the selected pay period.
    reference_days = (
        policy.get("standard_working_days_per_month")
        or attendance["working_days"]
        or 1
    )

    paid_leaves_allowed = round(
        policy["paid_leaves_allowed_per_month"]
        * (attendance["working_days"] / reference_days)
    )

    # Calculate leave deduction
    unpaid_days = max(
        0,
        (attendance["leaves"] + attendance["absent_days"])
        - paid_leaves_allowed,
    )

    leave_deduction = round(unpaid_days * per_day_rate, 2)

    # caalculate late arrival deduction
    late_arrival_deduction = round(
        attendance["late_arrival_hours"] * hourly_rate,
        2,
    )

    return leave_deduction, late_arrival_deduction


# calculate deduction rules like tax or UIF.
def generate_deduction_rules(employee: dict, gross_salary: float):

    line_items = []

    for rule in employee.get("deduction_rules", []):

        amount = _calc_rule_amount(
            rule["amount_type"],
            rule["amount"],
            gross_salary,
        )

        line_items.append(
            {
                "component": rule["deduction_type"],
                "type": "Deduction",
                "amount": amount,
            }
        )

    return line_items


# calculate complete payroll for an employee
def calculate_payroll(employee: dict, attendance: dict):

    #Calculate salary values
    basic_salary, overtime_pay, per_day_rate, hourly_rate = generate_salary(
        employee,
        attendance,
    )

    #calculate attendance deductions
    leave_deduction, late_arrival_deduction = (
        generate_attendance_deductions(
            employee,
            attendance,
            per_day_rate,
            hourly_rate,
        )
    )

    # calculate gross salary
    gross_salary = round(basic_salary + overtime_pay, 2)

    include_allowance_overtime = employee["salary_rule"][
        "include_allowance_and_overtime_in_payroll"
    ]

    payroll_calculation = [
        {
            "component": "Basic Salary",
            "type": "Earnings",
            "amount": basic_salary,
        }
    ]

    # add overtime if enabled
    if include_allowance_overtime and overtime_pay:
        payroll_calculation.append(
            {
                "component": "Overtime Pay",
                "type": "Earnings",
                "amount": overtime_pay,
            }
        )

    allowance_items = []

    # add allowances if enabled.
    if include_allowance_overtime:
        allowance_items = generate_allowances(employee, gross_salary)
        payroll_calculation.extend(allowance_items)

    # add attendance deductions.
    if leave_deduction:
        payroll_calculation.append(
            {
                "component": "Leave Deduction",
                "type": "Deduction",
                "amount": leave_deduction,
            }
        )

    if late_arrival_deduction:
        payroll_calculation.append(
            {
                "component": "Late Arrivals",
                "type": "Deduction",
                "amount": late_arrival_deduction,
            }
        )

    # add deduction rules.
    rule_deductions = generate_deduction_rules(employee, gross_salary)
    payroll_calculation.extend(rule_deductions)

    # calculate totals
    total_earnings = round(
        sum(
            item["amount"]
            for item in payroll_calculation
            if item["type"] == "Earnings"
        ),
        2,
    )

    total_deductions = round(
        leave_deduction
        + late_arrival_deduction
        + sum(item["amount"] for item in rule_deductions),
        2,
    )

    total_allowance = round(
        sum(item["amount"] for item in allowance_items),
        2,
    )

    net_salary = round(
        total_earnings - total_deductions,
        2,
    )

    return {
        "payroll_calculation": payroll_calculation,
        "gross_salary": gross_salary,
        "total_earnings": total_earnings,
        "total_deductions": total_deductions,
        "total_allowance": total_allowance,
        "net_salary": net_salary,
    }


# generte complete payroll response for one employee
# attendance is now a pre-fetched summary dict (from attendance_controller.get_attendance_summary),
# not generated from the employee doc.
def generate_employee_payroll(employee: dict, attendance: dict):

    payroll = calculate_payroll(employee, attendance)

    return {
        "emp_id": employee["emp_id"],
        "emp_name": employee["emp_name"],
        "email": employee["email"],
        "profile_image": employee["profile_image"],
        "department": employee["department"],
        "designation": employee["designation"],
        "status": "Pending",
        "payroll_calculation": payroll["payroll_calculation"],
        "attendance_summary": {
            "working_days": attendance["working_days"],
            "present_days": attendance["present_days"],
            "leaves": attendance["leaves"],
            "absent_days": attendance["absent_days"],
            "overtime_hours": attendance["overtime_hours"],
            "late_arrival_hours": attendance["late_arrival_hours"],
        },
        "gross_salary": payroll["gross_salary"],
        "total_earnings": payroll["total_earnings"],
        "total_deductions": payroll["total_deductions"],
        "total_allowance": payroll["total_allowance"],
        "net_salary": payroll["net_salary"],
    }