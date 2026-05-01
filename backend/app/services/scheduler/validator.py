from typing import List, Dict
from datetime import date, timedelta
from app.models.staff import Staff
from app.core.constants import ShiftType, MIN_NIGHT_SHIFTS, MAX_NIGHT_SHIFTS
from app.services.scheduler.constraints import ConstraintChecker

class ScheduleValidator:
    def __init__(self, schedule_matrix: Dict[date, Dict[int, ShiftType]], 
                 staff_list: List[Staff], night_count: Dict[int, int], 
                 rest_until: Dict[int, date]):
        self.schedule_matrix = schedule_matrix
        self.staff_list = staff_list
        self.night_count = night_count
        self.rest_until = rest_until
        self.violations: List[str] = []
    
    def validate(self) -> Dict:
        """Validate entire schedule against all rules"""
        self.violations = []
        
        self._check_coverage()
        self._check_night_rules()
        self._check_rest_periods()
        self._check_fairness()
        self._check_shift_conflicts()
        
        return {
            "valid": len(self.violations) == 0,
            "violations": self.violations,
            "night_counts": self.night_count
        }
    
    def _check_coverage(self):
        """Check each day has required shifts"""
        for day, staff_shifts in self.schedule_matrix.items():
            is_weekend = day.weekday() >= 5
            if not ConstraintChecker.check_coverage(day, self.schedule_matrix, is_weekend):
                self.violations.append(f"Coverage missing on {day}")
    
    def _check_night_rules(self):
        """Check night shift rules"""
        for day, staff_shifts in self.schedule_matrix.items():
            for staff_id, shift_type in staff_shifts.items():
                if shift_type == ShiftType.NIGHT:
                    # Check 2 consecutive nights
                    if ConstraintChecker.check_2_consecutive_nights(staff_id, day, self.schedule_matrix):
                        # Check 2 OFF days after
                        for offset in [2, 3]:
                            rest_day = day + timedelta(days=offset)
                            if rest_day in self.schedule_matrix:
                                if staff_id not in self.schedule_matrix[rest_day] or \
                                   self.schedule_matrix[rest_day][staff_id] != ShiftType.OFF:
                                    self.violations.append(
                                        f"Staff {staff_id} missing OFF on {rest_day} after 2 consecutive nights"
                                    )
    
    def _check_rest_periods(self):
        """Check staff in rest period are not assigned shifts"""
        for day, staff_shifts in self.schedule_matrix.items():
            for staff_id, shift_type in staff_shifts.items():
                if shift_type == ShiftType.OFF:
                    continue
                if self.rest_until.get(staff_id, date.min) > day:
                    self.violations.append(
                        f"Staff {staff_id} assigned shift on {day} during rest period"
                    )
    
    def _check_fairness(self):
        """Check fairness constraints"""
        if not ConstraintChecker.check_fairness(self.night_count, self.staff_list):
            self.violations.append("Night shift fairness constraints violated (min 8, max 10)")
    
    def _check_shift_conflicts(self):
        """Check one shift per day per staff"""
        for day, staff_shifts in self.schedule_matrix.items():
            # Count shifts per staff per day (should be max 1)
            staff_counts = {}
            for staff_id in staff_shifts.keys():
                staff_counts[staff_id] = staff_counts.get(staff_id, 0) + 1
            
            for staff_id, count in staff_counts.items():
                if count > 1:
                    self.violations.append(f"Staff {staff_id} has multiple shifts on {day}")
