# Import all models so SQLAlchemy mappers initialize properly
from app.models.staff import Staff
from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry
from app.models.night_tracking import NightTracking
from app.models.shift import Shift
from app.models.user import User
