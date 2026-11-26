from fastapi import APIRouter

from modules.departments.router import router as departments_router
from modules.departments.router import job_router

router = APIRouter(prefix="/api/v1")
router.include_router(departments_router)
router.include_router(job_router)
