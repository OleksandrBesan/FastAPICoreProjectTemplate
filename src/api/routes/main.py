from fastapi import APIRouter

from api.routes.test import router as test 

router = APIRouter()
router.include_router(test)  