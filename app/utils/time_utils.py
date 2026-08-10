from datetime import datetime, timedelta, date


def time_str_to_minutes(time_str: str) -> int:
    t = datetime.strptime(time_str, "%H:%M")
    return t.hour * 60 + t.minute


def time_str_to_hours(time_str: str) -> float:
    return time_str_to_minutes(time_str) / 60


DAY_NAME_TO_WEEKDAY = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
    "Friday": 4, "Saturday": 5, "Sunday": 6,
}


def count_working_days(start: date, end: date, weekend_days: list[str]) -> int:
    weekend_indices = {DAY_NAME_TO_WEEKDAY[d] for d in weekend_days if d in DAY_NAME_TO_WEEKDAY}
    total_days = (end - start).days + 1
    return sum(
        1 for i in range(total_days)
        if (start + timedelta(days=i)).weekday() not in weekend_indices
    )