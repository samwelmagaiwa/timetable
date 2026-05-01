from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schedule import Schedule, ScheduleCreate, ScheduleGenerateRequest, ScheduleUpdate
from app.schemas.schedule_entry import ScheduleEntry, ScheduleEntryUpdate
from app.services.schedule_service import ScheduleService

router = APIRouter()

@router.get("/", response_model=List[Schedule])
async def list_schedules(db: Session = Depends(get_db)):
    return ScheduleService(db).get_all()

@router.get("/month/{year}/{month}", response_model=List[Schedule])
async def get_schedules_by_month(year: int, month: int, db: Session = Depends(get_db)):
    return ScheduleService(db).get_by_month(year, month)

@router.post("/", response_model=Schedule)
async def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    return ScheduleService(db).create(schedule)

@router.get("/{schedule_id}", response_model=Schedule)
async def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = ScheduleService(db).get_by_id(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@router.put("/{schedule_id}", response_model=Schedule)
async def update_schedule(schedule_id: int, update: ScheduleUpdate, db: Session = Depends(get_db)):
    schedule = ScheduleService(db).update(schedule_id, update)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@router.put("/{schedule_id}/lock", response_model=Schedule)
async def lock_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = ScheduleService(db).lock(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@router.post("/generate", response_model=dict)
async def generate_schedule(request: ScheduleGenerateRequest, db: Session = Depends(get_db)):
    return ScheduleService(db).generate(request)

@router.put("/shift/{entry_id}", response_model=ScheduleEntry)
async def update_shift(entry_id: int, update: ScheduleEntryUpdate, db: Session = Depends(get_db)):
    entry = ScheduleService(db).update_shift(entry_id, update)
    if not entry:
        raise HTTPException(status_code=404, detail="Shift entry not found")
    return entry

@router.get("/{schedule_id}/entries")
async def get_schedule_entries(schedule_id: int, db: Session = Depends(get_db)):
    from app.models.schedule_entry import ScheduleEntry
    entries = db.query(ScheduleEntry).filter(ScheduleEntry.schedule_id == schedule_id).all()
    # Explicitly serialize dates as strings to avoid any client-side shift
    return [
        {
            "id": e.id,
            "schedule_id": e.schedule_id,
            "staff_id": e.staff_id,
            "date": e.date.isoformat(),
            "day_of_week": e.day_of_week.value,
            "shift_type": e.shift_type.value
        }
        for e in entries
    ]
