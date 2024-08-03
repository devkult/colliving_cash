from fastapi import APIRouter
from application.api.colliving.house.handlers import router as house_router
from application.api.colliving.users.handlers import router as users_router
from application.api.colliving.room.handlers import router as room_router

router = APIRouter()
router.include_router(house_router, tags=["House"], prefix="/house")
router.include_router(users_router, tags=["Users"], prefix="/users")
router.include_router(room_router, tags=["Room"], prefix="/room")
