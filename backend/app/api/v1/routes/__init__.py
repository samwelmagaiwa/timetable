from .users import router as users_router
from .staff import router as staff_router
from .schedule import router as schedule_router

__all__ = ["users_router", "staff_router", "schedule_router"]
