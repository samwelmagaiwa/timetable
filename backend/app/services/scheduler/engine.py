from typing import List, Dict, Tuple, Optional
from datetime import date, timedelta, datetime
from collections import defaultdict
from app.models.staff import Staff
from app.models.schedule_entry import ScheduleEntry
from app.models.night_tracking import NightTracking
from app.core.constants import ShiftType, DayOfWeek, MIN_NIGHT_SHIFTS, MAX_NIGHT_SHIFTS
from app.core.constants import DEFAULT_WEEKDAY_NIGHT_STAFF, DEFAULT_WEEKEND_NIGHT_STAFF
from app.services.scheduler.constraints import ConstraintChecker
from app.services.scheduler.heuristics import FairnessHeuristics

class SchedulerEngine:
    def __init__(self, db, staff_list: List[Staff], start_date: date, end_date: date, schedule_id: int):
        self.db = db
        self.staff_list = staff_list
        self.staff_ids = [s.id for s in staff_list]
        self.start_date = start_date
        self.end_date = end_date
        self.schedule_id = schedule_id
        
        # Initialize tracking structures
        self.schedule_matrix: Dict[date, Dict[int, ShiftType]] = defaultdict(dict)  # date → {staff_id: shift_type}
        self.night_count: Dict[int, int] = defaultdict(int)  # staff_id → night count
        self.rest_until: Dict[int, date] = defaultdict(lambda: date.min)  # staff_id → rest until date
        self.last_night_day: Dict[int, Optional[date]] = defaultdict(lambda: None)  # staff_id → last night shift date
        self.workload: Dict[int, int] = defaultdict(int)  # staff_id → total shifts assigned
        
        # Initialize night tracking from DB
        self._init_night_tracking()
    
    def _init_night_tracking(self):
        """Load existing night tracking for this schedule"""
        from app.models.night_tracking import NightTracking
        tracking = self.db.query(NightTracking).filter(
            NightTracking.schedule_id == self.schedule_id
        ).all()
        for t in tracking:
            self.night_count[t.staff_id] = t.night_count
            self.rest_until[t.staff_id] = t.rest_until if t.rest_until else date.min
            self.last_night_day[t.staff_id] = t.last_night_day
    
    def generate_schedule(self) -> List[ScheduleEntry]:
        """Generate full schedule"""
        # Step 1: Pre-initialize matrix keys
        self.schedule_matrix = {
            self.start_date + timedelta(days=i): {} 
            for i in range((self.end_date - self.start_date).days + 1)
        }
        
        # Step 2: Night Shifts
        self._assign_night_shifts()
        
        # Step 3: Constraints
        self._apply_night_constraints()
        
        # Step 4: Assign Weekend Shifts (M + E)
        self._assign_weekend_shifts()
        
        # Step 5: Assign Weekday Shifts
        self._assign_weekday_shifts()
        
        # Step 6: Gap Filling
        self._fill_gaps()
        
        # Step 7: Optimization Phase
        self._optimize_schedule()
        
        # Save to database
        return self._save_to_db()
    
    def _get_day_type(self, day: date) -> DayOfWeek:
        """Get day of week type"""
        from app.core.constants import DayOfWeek
        days = {
            0: DayOfWeek.MONDAY,
            1: DayOfWeek.TUESDAY,
            2: DayOfWeek.WEDNESDAY,
            3: DayOfWeek.THURSDAY,
            4: DayOfWeek.FRIDAY,
            5: DayOfWeek.SATURDAY,
            6: DayOfWeek.SUNDAY
        }
        return days[day.weekday()]
    
    def _is_weekend(self, day: date) -> bool:
        """Check if day is weekend (Sat/Sun)"""
        return day.weekday() >= 5
    
    def _assign_night_shifts(self):
        """Step 2: Assign Night Shifts FIRST in 2-day blocks"""
        current_date = self.start_date
        while current_date <= self.end_date:
            is_weekend = self._is_weekend(current_date)
            num_night_staff = DEFAULT_WEEKEND_NIGHT_STAFF if is_weekend else DEFAULT_WEEKDAY_NIGHT_STAFF
            
            yesterday = current_date - timedelta(days=1)
            day_before_yesterday = yesterday - timedelta(days=1)
            assigned_today = []
            
            # 1. Complete blocks for staff who worked ONLY YESTERDAY
            if yesterday in self.schedule_matrix:
                for staff_id, shift in self.schedule_matrix[yesterday].items():
                    if shift == ShiftType.NIGHT:
                        # Check if they also worked 2 days ago
                        worked_night_before = False
                        if day_before_yesterday in self.schedule_matrix:
                            if self.schedule_matrix[day_before_yesterday].get(staff_id) == ShiftType.NIGHT:
                                worked_night_before = True
                        
                        if not worked_night_before:
                            # They need their 2nd night to complete the block
                            self.schedule_matrix[current_date][staff_id] = ShiftType.NIGHT
                            self.night_count[staff_id] += 1
                            self.last_night_day[staff_id] = current_date
                            self.workload[staff_id] += 1
                            assigned_today.append(staff_id)

            # 2. Fill remaining slots with NEW blocks
            needed = num_night_staff - len(assigned_today)
            if needed > 0:
                candidates = self._get_night_candidates(current_date, needed)
                # Filter out those who were already assigned today
                available = [sid for sid in candidates if sid not in assigned_today]
                
                # Further filter: don't start a NEW block if they worked yesterday 
                # (prevents accidental 3-night chains or weird overlaps)
                available = [sid for sid in available if self.last_night_day[sid] != yesterday]
                
                for staff_id in available[:needed]:
                    self.schedule_matrix[current_date][staff_id] = ShiftType.NIGHT
                    self.night_count[staff_id] += 1
                    self.last_night_day[staff_id] = current_date
                    self.workload[staff_id] += 1
                    assigned_today.append(staff_id)
            
            current_date += timedelta(days=1)
    
    def _get_night_candidates(self, day: date, num_needed: int) -> List[int]:
        """Get eligible candidates for night shift"""
        candidates = []
        for staff in self.staff_list:
            staff_id = staff.id
            # Check if staff is in rest period
            if self.rest_until[staff_id] > day:
                continue
            # Check night shift eligibility
            eligible = getattr(staff, 'can_work_night_shift', True)
            if not eligible:
                # print(f"DEBUG: Staff {staff.name} (ID {staff_id}) is NOT eligible for night shifts")
                continue
            # Check night shift limits
            if self.night_count[staff_id] >= MAX_NIGHT_SHIFTS:
                continue
            # Check 2 consecutive nights
            if self.last_night_day[staff_id] == day - timedelta(days=1):
                # Check if had night shift 2 days ago too
                if self.last_night_day[staff_id] and (day - timedelta(days=2)) in [
                    d for d, s in self.schedule_matrix.items() 
                    if s.get(staff_id) == ShiftType.NIGHT
                ]:
                    continue
            candidates.append(staff_id)
        
        # Rank candidates: lowest night_count, then longest since last night
        candidates.sort(key=lambda sid: (
            self.night_count[sid],
            self.last_night_day[sid] if self.last_night_day[sid] else date.min
        ))
        return candidates
    
    def _apply_night_constraints(self):
        """Step 3: Apply Night Constraints"""
        for day, staff_shifts in self.schedule_matrix.items():
            for staff_id, shift_type in staff_shifts.items():
                if shift_type == ShiftType.NIGHT:
                    # Next day: disallow Morning
                    next_day = day + timedelta(days=1)
                    if next_day <= self.end_date:
                        # Mark that staff can't work Morning next day
                        # This is handled during shift assignment
                        pass
                    
                    # Check 2 consecutive nights
                    prev_day = day - timedelta(days=1)
                    if (prev_day in self.schedule_matrix and 
                        self.schedule_matrix[prev_day].get(staff_id) == ShiftType.NIGHT):
                        # 2 consecutive nights: rest for 1 day (Day+1 is OFF)
                        # We rest UNTIL start of Day+2
                        self.rest_until[staff_id] = day + timedelta(days=2)
                        # Set OFF for Day+1
                        rest_day = day + timedelta(days=1)
                        if rest_day <= self.end_date:
                            self.schedule_matrix[rest_day][staff_id] = ShiftType.OFF
    
    def _assign_weekend_shifts(self):
        """Step 4: Assign Weekend Shifts (M + E)"""
        current_date = self.start_date
        while current_date <= self.end_date:
            if not self._is_weekend(current_date):
                current_date += timedelta(days=1)
                continue
            
            # Assign 1 Morning and 1 Evening shift
            for shift_type in [ShiftType.MORNING, ShiftType.EVENING]:
                self._assign_shift_for_day(current_date, shift_type)
            
            current_date += timedelta(days=1)
    
    def _assign_weekday_shifts(self):
        """Step 5: Assign Weekday Shifts - ALL available staff get Normal Day duty"""
        current_date = self.start_date
        while current_date <= self.end_date:
            if self._is_weekend(current_date):
                current_date += timedelta(days=1)
                continue
            
            # Assign ALL eligible staff to Normal Day shift
            for staff in self.staff_list:
                staff_id = staff.id
                
                # Skip if already assigned (night shift or OFF)
                if staff_id in self.schedule_matrix[current_date]:
                    continue
                
                # Skip if had night shift previous day (need rest)
                prev_day = current_date - timedelta(days=1)
                if (prev_day in self.schedule_matrix and 
                    self.schedule_matrix[prev_day].get(staff_id) == ShiftType.NIGHT):
                    continue
                
                self.schedule_matrix[current_date][staff_id] = ShiftType.NORMAL
                self.workload[staff_id] += 1
            
            current_date += timedelta(days=1)
    
    def _assign_shift_for_day(self, day: date, shift_type: ShiftType):
        """Assign a single shift for a day, selecting least workload staff"""
        # Get eligible staff
        eligible = []
        for staff in self.staff_list:
            staff_id = staff.id
            # Check if already assigned that day
            if staff_id in self.schedule_matrix[day]:
                continue
            
            # Check Morning after Night constraint
            if shift_type == ShiftType.MORNING:
                prev_day = day - timedelta(days=1)
                if (prev_day in self.schedule_matrix and 
                    self.schedule_matrix[prev_day].get(staff_id) == ShiftType.NIGHT):
                    continue
            
            eligible.append(staff_id)
        
        if not eligible:
            return
        
        # Select staff with least workload
        selected = min(eligible, key=lambda sid: self.workload[sid])
        
        # Assign shift
        self.schedule_matrix[day][selected] = shift_type
        self.workload[selected] += 1
    
    def _fill_gaps(self):
        """Step 6: Gap Filling - fill any unassigned required shifts"""
        current_date = self.start_date
        while current_date <= self.end_date:
            # Check if day has all required shifts
            day_shifts = self.schedule_matrix[current_date]
            required = self._get_required_shifts(current_date)
            
            for shift_type, count in required.items():
                assigned = sum(1 for s in day_shifts.values() if s == shift_type)
                if assigned < count:
                    # Fill missing shifts
                    for _ in range(count - assigned):
                        self._assign_shift_for_day(current_date, shift_type)
            
            current_date += timedelta(days=1)
    
    def _get_required_shifts(self, day: date) -> Dict[ShiftType, int]:
        """Get required shift counts for a day"""
        if self._is_weekend(day):
            return {
                ShiftType.MORNING: 1,
                ShiftType.EVENING: 1,
                ShiftType.NIGHT: DEFAULT_WEEKEND_NIGHT_STAFF
            }
        else:
            return {
                ShiftType.NIGHT: DEFAULT_WEEKDAY_NIGHT_STAFF
            }
    
    def _optimize_schedule(self):
        """Step 7: Optimization Phase - swap shifts to improve fairness"""
        # Simple optimization: swap night shifts between staff to balance night counts
        for _ in range(10):  # Run iterative improvement
            improved = False
            for day, staff_shifts in self.schedule_matrix.items():
                for staff_id, shift_type in list(staff_shifts.items()):
                    if shift_type != ShiftType.NIGHT:
                        continue
                    
                    # Find staff with lower night count to swap with
                    for other_staff in self.staff_list:
                        other_id = other_staff.id
                        if other_id == staff_id:
                            continue
                        if self.night_count[other_id] < self.night_count[staff_id] - 1:
                            # Swap night shifts if eligible
                            if self._can_swap_night(day, staff_id, other_id):
                                self._swap_night_shift(day, staff_id, other_id)
                                improved = True
                                break
            if not improved:
                break
    
    def _can_swap_night(self, day: date, staff1_id: int, staff2_id: int) -> bool:
        """Check if two staff can swap night shifts"""
        # Check if staff2 is eligible for night shift on day
        if self.rest_until[staff2_id] > day:
            return False
        if self.night_count[staff2_id] >= MAX_NIGHT_SHIFTS:
            return False
        
        # Check eligibility flag
        staff2 = next((s for s in self.staff_list if s.id == staff2_id), None)
        if staff2 and not getattr(staff2, 'can_work_night_shift', True):
            return False
            
        return True
    
    def _swap_night_shift(self, day: date, staff1_id: int, staff2_id: int):
        """Swap night shift between two staff"""
        self.schedule_matrix[day][staff1_id] = ShiftType.OFF
        self.schedule_matrix[day][staff2_id] = ShiftType.NIGHT
        self.night_count[staff1_id] -= 1
        self.night_count[staff2_id] += 1
        self.workload[staff1_id] -= 1
        self.workload[staff2_id] += 1
    
    def _save_to_db(self) -> List[ScheduleEntry]:
        """Save generated schedule to database"""
        entries = []
        for day, staff_shifts in self.schedule_matrix.items():
            for staff_id, shift_type in staff_shifts.items():
                if shift_type == ShiftType.OFF:
                    continue
                entry = ScheduleEntry(
                    schedule_id=self.schedule_id,
                    staff_id=staff_id,
                    date=day,
                    day_of_week=self._get_day_type(day),
                    shift_type=shift_type
                )
                self.db.add(entry)
                entries.append(entry)
        
        # Update night tracking
        for staff in self.staff_list:
            staff_id = staff.id
            tracking = self.db.query(NightTracking).filter(
                NightTracking.staff_id == staff_id,
                NightTracking.schedule_id == self.schedule_id
            ).first()
            if not tracking:
                tracking = NightTracking(
                    staff_id=staff_id,
                    schedule_id=self.schedule_id,
                    night_count=self.night_count[staff_id],
                    last_night_day=self.last_night_day[staff_id],
                    rest_until=self.rest_until[staff_id] if self.rest_until[staff_id] != date.min else None
                )
                self.db.add(tracking)
            else:
                tracking.night_count = self.night_count[staff_id]
                tracking.last_night_day = self.last_night_day[staff_id]
                tracking.rest_until = self.rest_until[staff_id] if self.rest_until[staff_id] != date.min else None
        
        self.db.commit()
        return entries
