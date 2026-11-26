from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.session import get_db
from modules.employees import services
from modules.employees.schemas import (
    WorkAreaCreate, 
    WorkAreaRead,
    EmployeeCreate,
    EmployeeRead
)

work_area_router = APIRouter(prefix="/work-areas", tags=["work-areas"])
employee_router = APIRouter(prefix="/employees", tags=["employees"])
Database = Annotated[Session, Depends(get_db)]

@work_area_router.get("", response_model=list[WorkAreaRead])
def list_work_areas(db: Database):
    return services.list_work_areas(db)

@work_area_router.post("", response_model=WorkAreaRead, status_code=201)
def create_work_area(data: WorkAreaCreate, db: Database):
    return services.create_work_area(db, data)

@employee_router.post("", response_model=EmployeeRead, status_code=201)
def create_employee(data: EmployeeCreate, db: Database):
    try:
        return services.create_employee(db, data)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except IntegrityError as error:
        if isinstance(error.orig, UniqueViolation):
            raise HTTPException(
                status_code=409,
                detail="Employee data already exists",
            ) from error
        raise

@employee_router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: str, db: Database):
    employee = services.get_employee(db, employee_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee