from aiogram import Router


from .start_booking import router as start_router
from .booking_service import router as service_router
from .booking_calendar import router as calendar_router
from .booking_time_handler import router as time_router
from .booking_request import router as confirm_router


booking_router = Router()

booking_router.include_router(start_router)
booking_router.include_router(service_router)
booking_router.include_router(calendar_router)
booking_router.include_router(time_router)
booking_router.include_router(confirm_router)
