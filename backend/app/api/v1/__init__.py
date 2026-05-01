from fastapi import APIRouter
from app.api.v1.routes import users, staff, schedule

router = APIRouter(prefix="/api/v1")

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(staff.router, prefix="/staff", tags=["staff"])
router.include_router(schedule.router, prefix="/schedules", tags=["schedules"])
