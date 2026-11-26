from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from modules.departments.models import Department, Job
from modules.departments.schemas import DepartmentCreate, JobCreate

def list_department(db: Session) -> list[Department]:
    query = select(Department).order_by(Department.name, Department.id)
    departments = db.scalars(query)
    return list(departments)

def create_department(db: Session, data: DepartmentCreate) -> Department | None:
    department = Department(
        name=data.name,
        cost_center_code=data.cost_center_code
    )
    db.add(department)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        query = select(Department.id).where(
            Department.cost_center_code == data.cost_center_code
        )
        existing_id = db.scalar(query)
        if existing_id is not None:
            return None
        raise

    db.refresh(department)
    return department

def list_jobs(db: Session) -> list[Job]:
    query = select(Job).order_by(Job.name, Job.id)
    jobs = db.scalars(query)
    return list(jobs)

def create_job(db: Session, data: JobCreate) -> Job | None:
    department = db.get(Department, data.department_id)
    if department is None:
        return None

    job = Job(
        department_id=data.department_id,
        name=data.name,
        allowance=data.allowance
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    return job