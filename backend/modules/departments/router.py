from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from modules.departments import services
from modules.departments.schemas import (
    DepartmentCreate, 
    DepartmentRead,
    JobCreate,
    JobRead
)

router = APIRouter(prefix="/departments", tags=["departments"])
job_router = APIRouter(prefix="/jobs", tags=["jobs"])
Database = Annotated[Session, Depends(get_db)]

@router.get("", response_model=list[DepartmentRead])
def list_departments(db: Database):
    return services.list_department(db)

@router.post("", response_model=DepartmentRead, status_code=201)
def create_department(data: DepartmentCreate, db: Database):
    department = services.create_department(db, data)
    if department is None:
        raise HTTPException(
            status_code=409,
            detail="Cost center code already exists"
        )
    return department

@job_router.get("", response_model=list[JobRead])
def list_jobs(db: Database):
    return services.list_jobs(db)

@job_router.post("", response_model=JobRead, status_code=201)
def create_job(data: JobCreate, db: Database):
    job = services.create_job(db, data)
    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )
    return job