from typing import List, Dict
from datetime import date, timedelta
from app.core.constants import ShiftType, MIN_NIGHT_SHIFTS, MAX_NIGHT_SHIFTS
from app.services.scheduler.heuristics import FairnessHeuristics

class ScheduleOptimizer:
    def __init__(self, staff_list: List, schedule_matrix: Dict, night_count: Dict, workload: Dict, rest_until: Dict):
        self.staff_list = staff_list
        self.schedule_matrix = schedule_matrix
        self.night_count = night_count
        self.workload = workload
        self.rest_until = rest_until
    
    def optimize(self) -> Dict:
        """Run optimization to improve schedule fairness"""
        best_score = self._calculate_score()
        improved = True
        iterations = 0
        
        while improved and iterations < 100:
            improved = False
            iterations += 1
            
            # Try swapping night shifts between staff
            for day, staff_shifts in self.schedule_matrix.items():
                for staff_id, shift_type in list(staff_shifts.items()):
                    if shift_type != ShiftType.NIGHT:
                        continue
                    
                    # Find staff with lower night count
                    for other_staff in self.staff_list:
                        other_id = other_staff.id
                        if other_id == staff_id:
                            continue
                        
                        if self.night_count.get(other_id, 0) < self.night_count.get(staff_id, 0) - 1:
                            if self._can_swap(day, staff_id, other_id):
                                self._swap_night(day, staff_id, other_id)
                                new_score = self._calculate_score()
                                if new_score < best_score:
                                    best_score = new_score
                                    improved = True
                                    break
                                else:
                                    # Swap back
                                    self._swap_night(day, other_id, staff_id)
                    if improved:
                        break
        
        return self.schedule_matrix
    
    def _can_swap(self, day: date, staff1: int, staff2: int) -> bool:
        """Check if two staff can swap shifts"""
        # Check if staff2 is eligible for night shift
        if self.rest_until.get(staff2, date.min) > day:
            return False
        if self.night_count.get(staff2, 0) >= MAX_NIGHT_SHIFTS:
            return False
        return True
    
    def _swap_night(self, day: date, from_staff: int, to_staff: int):
        """Swap night shift between two staff"""
        self.schedule_matrix[day][from_staff] = ShiftType.OFF
        self.schedule_matrix[day][to_staff] = ShiftType.NIGHT
        self.night_count[from_staff] -= 1
        self.night_count[to_staff] += 1
        self.workload[from_staff] -= 1
        self.workload[to_staff] += 1
    
    def _calculate_score(self) -> float:
        """Calculate schedule score (lower is better)"""
        score = 0.0
        
        # Night imbalance penalty (weight: 10)
        score += FairnessHeuristics.calculate_night_imbalance(self.night_count) * 10
        
        # Workload imbalance penalty (weight: 5)
        score += FairnessHeuristics.calculate_workload_imbalance(self.schedule_matrix) * 5
        
        return score
