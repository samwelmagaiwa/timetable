from datetime import date, timedelta
from typing import List, Dict
from app.models.schedule_entry import ScheduleEntry
from app.models.staff import Staff
from app.core.constants import ShiftType, MIN_NIGHT_SHIFTS, MAX_NIGHT_SHIFTS

class ConstraintChecker:
    @staticmethod
    def check_night_shift_rules(staff_id: int, day: date, schedule_matrix: Dict[date, Dict[int, ShiftType]], 
                                night_count: Dict[int, int], rest_until: Dict[int, date]) -> bool:
        """Check if staff can work night shift on given day"""
        # Check rest period
        if rest_until.get(staff_id, date.min) > day:
            return False
        
        # Check max night shifts
        if night_count.get(staff_id, 0) >= MAX_NIGHT_SHIFTS:
            return False
        
        return True
    
    @staticmethod
    def check_morning_after_night(staff_id: int, day: date, schedule_matrix: Dict[date, Dict[int, ShiftType]]) -> bool:
        """Check if staff can work Morning shift (can't if worked Night previous day)"""
        prev_day = day - timedelta(days=1)
        if prev_day in schedule_matrix:
            if schedule_matrix[prev_day].get(staff_id) == ShiftType.NIGHT:
                return False
        return True
    
    @staticmethod
    def check_2_consecutive_nights(staff_id: int, day: date, schedule_matrix: Dict[date, Dict[int, ShiftType]]) -> bool:
        """Check if staff has 2 consecutive nights, requires 2 OFF days"""
        prev_day = day - timedelta(days=1)
        if (prev_day in schedule_matrix and 
            schedule_matrix[prev_day].get(staff_id) == ShiftType.NIGHT and
            schedule_matrix[day].get(staff_id) == ShiftType.NIGHT):
            return True
        return False
    
    @staticmethod
    def check_coverage(day: date, schedule_matrix: Dict[date, Dict[int, ShiftType]], 
                       is_weekend: bool) -> bool:
        """Check if day has all required shifts"""
        from app.core.constants import DEFAULT_WEEKDAY_NIGHT_STAFF, DEFAULT_WEEKEND_NIGHT_STAFF
        
        day_shifts = schedule_matrix.get(day, {})
        shift_counts = {ShiftType.MORNING: 0, ShiftType.EVENING: 0, ShiftType.NIGHT: 0}
        
        for shift_type in day_shifts.values():
            if shift_type in shift_counts:
                shift_counts[shift_type] += 1
        
        # Check Morning (1 required)
        if shift_counts[ShiftType.MORNING] < 1:
            return False
        
        # Check Evening (1 required)
        if shift_counts[ShiftType.EVENING] < 1:
            return False
        
        # Check Night
        night_required = DEFAULT_WEEKEND_NIGHT_STAFF if is_weekend else DEFAULT_WEEKDAY_NIGHT_STAFF
        if shift_counts[ShiftType.NIGHT] < night_required:
            return False
        
        return True
    
    @staticmethod
    def check_fairness(night_count: Dict[int, int], staff_list: List[Staff]) -> bool:
        """Check if night shifts are fairly distributed"""
        for staff in staff_list:
            count = night_count.get(staff.id, 0)
            if count < MIN_NIGHT_SHIFTS or count > MAX_NIGHT_SHIFTS:
                return False
        return True
