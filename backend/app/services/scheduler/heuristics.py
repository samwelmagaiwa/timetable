from typing import List, Dict
from datetime import date
from collections import Counter
from app.models.staff import Staff
from app.models.schedule_entry import ScheduleEntry
from app.core.constants import ShiftType

class FairnessHeuristics:
    @staticmethod
    def calculate_staff_workload(staff_id: int, schedule_matrix: Dict[date, Dict[int, ShiftType]]) -> int:
        """Calculate total shifts assigned to staff"""
        workload = 0
        for day_shifts in schedule_matrix.values():
            if staff_id in day_shifts:
                workload += 1
        return workload
    
    @staticmethod
    def get_least_assigned_staff(staff_list: List[Staff], schedule_matrix: Dict[date, Dict[int, ShiftType]], 
                                  rest_until: Dict[int, date], current_day: date) -> int:
        """Get staff with least workload who is available"""
        candidates = []
        for staff in staff_list:
            staff_id = staff.id
            # Check if in rest
            if rest_until.get(staff_id, date.min) > current_day:
                continue
            # Check if already assigned that day
            if staff_id in schedule_matrix.get(current_day, {}):
                continue
            workload = FairnessHeuristics.calculate_staff_workload(staff_id, schedule_matrix)
            candidates.append((staff_id, workload))
        
        if not candidates:
            return -1
        
        # Return staff with least workload
        return min(candidates, key=lambda x: x[1])[0]
    
    @staticmethod
    def calculate_night_imbalance(night_count: Dict[int, int]) -> float:
        """Calculate how imbalanced night shifts are (lower is better)"""
        if not night_count:
            return 0.0
        counts = list(night_count.values())
        return max(counts) - min(counts) if counts else 0.0
    
    @staticmethod
    def calculate_workload_imbalance(schedule_matrix: Dict[date, Dict[int, ShiftType]]) -> float:
        """Calculate workload imbalance (lower is better)"""
        workloads = []
        for day_shifts in schedule_matrix.values():
            for staff_id in day_shifts.keys():
                workloads.append(staff_id)
        
        if not workloads:
            return 0.0
        
        from collections import Counter
        counts = Counter(workloads)
        if not counts:
            return 0.0
        return max(counts.values()) - min(counts.values())
