from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from modules.departments.models import Job
from modules.recruitment.models import Applicant
from modules.employees.models import WorkArea, Employee
from modules.employees.schemas import WorkAreaCreate, EmployeeCreate

def list_work_areas(db: Session) -> list[WorkArea]:
    query = select(WorkArea).order_by(WorkArea.name, WorkArea.id)
    areas = db.scalars(query)
    return list(areas)

def create_work_area(db: Session, data: WorkAreaCreate) -> WorkArea | None:
    work_area = WorkArea(
        name=data.name,
        city=data.city,
        location_type=data.location_type
    )

    db.add(work_area)
    db.commit()
    db.refresh(work_area)
    return work_area

def get_employee(db: Session, employee_id: str):
    return db.get(Employee, employee_id)

def create_employee(db: Session, data: EmployeeCreate) -> Employee | None:
    if db.get(Job, data.job_id) is None:
        raise ValueError("Job not found")
    if db.get(WorkArea, data.work_area_id) is None:
        raise ValueError("Work area not found")
    if data.manager_id is not None:
        if db.get(Employee, data.manager_id) is None:
            raise ValueError("Manager not found")
        if data.applicant_id is not None:
            if db.get(Applicant, data.applicant_id) is None:
                raise ValueError("Applicant not found")

    employee = Employee(id=f"EMP-{uuid4().hex}", **data.model_dump())
    db.add(employee)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(employee)
    return employee