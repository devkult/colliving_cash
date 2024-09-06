from fastapi import APIRouter
from presentation.api.colliving.house.handlers import router as house_router
from presentation.api.colliving.users.handlers import router as users_router

router = APIRouter()
router.include_router(house_router, tags=["House"], prefix="/house")
router.include_router(users_router, tags=["Users"], prefix="/users")
