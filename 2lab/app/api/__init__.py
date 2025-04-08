from fastapi import APIRouter

router = APIRouter()

from .users import router as user_router
from .encoding import router as encoding_router

router.include_router(user_router)
router.include_router(encoding_router)