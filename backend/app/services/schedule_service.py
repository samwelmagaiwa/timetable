from sqlalchemy.orm import Session
from datetime import date
from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry
from app.schemas.schedule import ScheduleCreate, ScheduleGenerateRequest, ScheduleUpdate
from app.schemas.schedule_entry import ScheduleEntryUpdate
from app.services.scheduler.engine import SchedulerEngine

class ScheduleService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Schedule).all()
    
    def get_by_id(self, schedule_id: int):
        return self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
    
    def get_by_month(self, year: int, month: int):
        """Get schedules for a specific month"""
        start = date(year, month, 1)
        if month == 12:
            end = date(year+1, 1, 1) - date.resolution
        else:
            end = date(year, month+1, 1) - date.resolution
        return self.db.query(Schedule).filter(
            Schedule.start_date <= end,
            Schedule.end_date >= start
        ).all()
    
    def create(self, schedule: ScheduleCreate):
        db_schedule = Schedule(**schedule.model_dump())
        self.db.add(db_schedule)
        self.db.commit()
        self.db.refresh(db_schedule)
        return db_schedule
    
    def update(self, schedule_id: int, update: ScheduleUpdate):
        db_schedule = self.get_by_id(schedule_id)
        if not db_schedule:
            return None
        for key, value in update.model_dump(exclude_unset=True).items():
            setattr(db_schedule, key, value)
        self.db.commit()
        self.db.refresh(db_schedule)
        return db_schedule
    
    def lock(self, schedule_id: int):
        return self.update(schedule_id, ScheduleUpdate(is_locked=True))
    
    def generate(self, request: ScheduleGenerateRequest):
        from app.models.staff import Staff
        from app.schemas.schedule_entry import ScheduleEntry as ScheduleEntrySchema
        
        # Create schedule first
        schedule = Schedule(
            name=f"Schedule {request.start_date} to {request.end_date}",
            start_date=request.start_date,
            end_date=request.end_date
        )
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        
        # Get staff list
        query = self.db.query(Staff).filter(Staff.is_active == True)
        if request.staff_ids:
            query = query.filter(Staff.id.in_(request.staff_ids))
        staff_list = query.all()
        
        if not staff_list:
            return {
                "schedule": {
                    "id": schedule.id,
                    "name": schedule.name,
                    "start_date": str(schedule.start_date),
                    "end_date": str(schedule.end_date),
                    "is_locked": schedule.is_locked
                },
                "entries": [],
                "message": "No staff found"
            }
        
        # Run scheduler engine
        try:
            engine = SchedulerEngine(
                self.db, staff_list, 
                request.start_date, request.end_date, 
                schedule.id
            )
            entries = engine.generate_schedule()
            
            # Convert ORM entries to dicts for JSON serialization
            entry_dicts = []
            for entry in entries:
                entry_dicts.append({
                    "id": entry.id,
                    "schedule_id": entry.schedule_id,
                    "staff_id": entry.staff_id,
                    "date": str(entry.date),
                    "day_of_week": entry.day_of_week.value,
                    "shift_type": entry.shift_type.value
                })
            
            return {
                "schedule": {
                    "id": schedule.id,
                    "name": schedule.name,
                    "start_date": str(schedule.start_date),
                    "end_date": str(schedule.end_date),
                    "is_locked": schedule.is_locked
                },
                "entries": entry_dicts
            }
        except Exception as e:
            return {
                "schedule": {
                    "id": schedule.id,
                    "name": schedule.name,
                    "start_date": str(schedule.start_date),
                    "end_date": str(schedule.end_date),
                    "is_locked": schedule.is_locked
                },
                "entries": [],
                "error": str(e)
            }
    
    def update_shift(self, entry_id: int, update: ScheduleEntryUpdate):
        """Update a single shift entry"""
        entry = self.db.query(ScheduleEntry).filter(ScheduleEntry.id == entry_id).first()
        if not entry:
            return None
        for key, value in update.model_dump(exclude_unset=True).items():
            setattr(entry, key, value)
        self.db.commit()
        self.db.refresh(entry)
        return entry
