from fastapi import APIRouter

from modules.departments.router import router as departments_router
from modules.departments.router import job_router
from modules.employees.router import work_area_router, employee_router
from modules.recruitment.router import router as applicants_router

router = APIRouter(prefix="/api/v1")
router.include_router(departments_router)
router.include_router(job_router)
router.include_router(work_area_router)
router.include_router(employee_router)
router.include_router(applicants_router)
