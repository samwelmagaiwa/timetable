import pytest
from datetime import date, timedelta
from app.services.scheduler.engine import SchedulerEngine
from app.models.staff import Staff

def test_scheduler_engine_creation():
    staff = [Staff(id=1, name="John", role="nurse", max_hours_per_week=40)]
    start = date.today()
    end = start + timedelta(days=7)
    
    engine = SchedulerEngine(staff, start, end)
    assert engine is not None

def test_generate_schedule():
    staff = [Staff(id=1, name="John", role="nurse", max_hours_per_week=40)]
    start = date.today()
    end = start + timedelta(days=2)
    
    engine = SchedulerEngine(staff, start, end)
    shifts = engine.generate_schedule()
    assert isinstance(shifts, list)
