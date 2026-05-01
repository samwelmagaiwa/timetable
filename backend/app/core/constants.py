from enum import Enum
from datetime import time

class ShiftType(str, Enum):
    MORNING = "M"   # Morning: morning → 8 PM (20:00)
    EVENING = "E"    # Evening: 8 PM → 2 AM
    NIGHT = "N"      # Night shift
    NORMAL = "D"     # Normal weekday duty (all available staff)
    OFF = "O"        # Rest day

class DayOfWeek(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

class StaffRole(str, Enum):
    NURSE = "nurse"
    DOCTOR = "doctor"
    TECHNICIAN = "technician"
    ADMIN = "admin"

# Shift time mappings (as per AGENT.MD.txt)
SHIFT_TIMES = {
    ShiftType.MORNING: {"start": time(8, 0), "end": time(20, 0)},    # 8 AM → 8 PM
    ShiftType.EVENING: {"start": time(20, 0), "end": time(2, 0)},    # 8 PM → 2 AM next day
    ShiftType.NIGHT: {"start": time(22, 0), "end": time(6, 0)},      # 10 PM → 6 AM
    ShiftType.OFF: {"start": None, "end": None}
}

# Scheduling constants (from AGENT.MD.txt)
DEFAULT_WEEKDAY_NIGHT_STAFF = 2
DEFAULT_WEEKEND_NIGHT_STAFF = 2  # Configurable 1-2

# Fairness constraints
MIN_NIGHT_SHIFTS = 8
MAX_NIGHT_SHIFTS = 10

# Rest rules
REST_AFTER_NIGHT = 1  # Next day can't work Morning
REST_AFTER_2_CONSECUTIVE_NIGHTS = 2  # 2 consecutive OFF days