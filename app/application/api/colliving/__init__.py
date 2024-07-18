from fastapi import APIRouter
from application.api.colliving.house.handlers import router as house_router

router = APIRouter()
router.include_router(house_router, tags=["House"], prefix="/house")
