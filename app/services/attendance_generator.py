from datetime import date, datetime, timedelta

# convert time into hours so we can calculate late and overtime hours
def _time_str_to_hours(time_str: str) -> float:
     #Convert string into datetime object
    t = datetime.strptime(time_str, "%H:%M")
     # Return total hours (including minutes)
    return t.hour + (t.minute / 60)

#generate attendance record for each working day in the pay period
def generate_daily_attendance_log(employee: dict, pay_period_start: date, pay_period_end: date):

    # get employee attendance data and attndance rules.
    events = employee["attendance_events"]
    #get attendance policy
    policy = employee["salary_rule"]["attendance_policy"]
    standard_clock_in = policy["standard_clock_in"]
    standard_clock_out = policy["standard_clock_out"]

    leave_dates = set(events.get("leave_dates", []))
    absent_dates = set(events.get("absent_dates", []))
    late_clock_ins = events.get("late_clock_ins", {})
    overtime_clock_outs = events.get("overtime_clock_outs", {})

    daily_log = []
    total_days = (pay_period_end - pay_period_start).days + 1

    # loop through each day in the pay period.
    for i in range(total_days):
        current_date = pay_period_start + timedelta(days=i)

        # skip weekends because they are not working days.
        if current_date.weekday() >= 5: 
            continue

        date_str = current_date.isoformat()

        if date_str in leave_dates:
            daily_log.append(
                {
                    "date": date_str,
                    "status": "Leave",
                    "clock_in": None,
                    "clock_out": None,
                    "late_hours": 0.0,
                    "overtime_hours": 0.0,
                }
            )
            continue

        if date_str in absent_dates:
            daily_log.append(
                {
                    "date": date_str,
                    "status": "Absent",
                    "clock_in": None,
                    "clock_out": None,
                    "late_hours": 0.0,
                    "overtime_hours": 0.0,
                }
            )
            continue

        # get employees actual clock-in and clock-out time
        actual_clock_in = late_clock_ins.get(date_str, standard_clock_in)
        actual_clock_out = overtime_clock_outs.get(date_str, standard_clock_out)

        # calculate late arrival and overtime hours
        late_hours = max(
            0.0,
            round(
                _time_str_to_hours(actual_clock_in)
                - _time_str_to_hours(standard_clock_in),
                2,
            ),
        )

        overtime_hours = max(
            0.0,
            round(
                _time_str_to_hours(actual_clock_out)
                - _time_str_to_hours(standard_clock_out),
                2,
            ),
        )

        # save attendance for a present day
        daily_log.append(
            {
                "date": date_str,
                "status": "Present",
                "clock_in": actual_clock_in,
                "clock_out": actual_clock_out,
                "late_hours": late_hours,
                "overtime_hours": overtime_hours,
            }
        )

    return daily_log

#calculat attendance summary from the daily attendance log
def generate_attendance(employee: dict, pay_period_start: date, pay_period_end: date):

    #generate daily attendance records first
    daily_log = generate_daily_attendance_log(
        employee, pay_period_start, pay_period_end
    )

    #count attendance values
    working_days = len(daily_log)
    present_days = sum(1 for d in daily_log if d["status"] == "Present")
    leaves = sum(1 for d in daily_log if d["status"] == "Leave")
    absent_days = sum(1 for d in daily_log if d["status"] == "Absent")

    # add total overtime and late hours.
    overtime_hours = round(sum(d["overtime_hours"] for d in daily_log), 2)
    late_arrival_hours = round(sum(d["late_hours"] for d in daily_log), 2)

    return {
        "working_days": working_days,
        "present_days": present_days,
        "leaves": leaves,
        "absent_days": absent_days,
        "overtime_hours": overtime_hours,
        "late_arrival_hours": late_arrival_hours,
    }