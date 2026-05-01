from datetime import date, datetime, timedelta
from app.core.constants import DayOfWeek

def get_day_of_week(d: date) -> DayOfWeek:
    days = {
        0: DayOfWeek.MONDAY,
        1: DayOfWeek.TUESDAY,
        2: DayOfWeek.WEDNESDAY,
        3: DayOfWeek.THURSDAY,
        4: DayOfWeek.FRIDAY,
        5: DayOfWeek.SATURDAY,
        6: DayOfWeek.SUNDAY
    }
    return days[d.weekday()]

def get_dates_between(start: date, end: date) -> list[date]:
    delta = end - start
    return [start + timedelta(days=i) for i in range(delta.days + 1)]
