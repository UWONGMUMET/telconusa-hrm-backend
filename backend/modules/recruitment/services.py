from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.departments.models import Job
from modules.recruitment.models import Applicant, ApplicantSelection
from modules.recruitment.schemas import ApplicantCreate, SelectionCreate

def list_applicants(db: Session) -> list[Applicant]:
    query = select(Applicant).order_by(Applicant.id)
    applicants = db.scalars(query)
    return list(applicants)

def create_applicant(db: Session, data: ApplicantCreate) -> Applicant | None:
    job = db.get(Job, data.job_id)
    if job is None:
        return None

    applicant = Applicant(
        job_id=data.job_id,
        full_name=data.full_name,
        contact=data.contact,
        application_status=data.application_status
    )

    db.add(applicant)
    db.commit()
    db.refresh(applicant)
    return applicant

def list_selection(db: Session, applicant_id: int) -> list[ApplicantSelection] | None:
    applicant = db.get(Applicant, applicant_id)
    if applicant is None:
        return None

    query = select(ApplicantSelection).where(
        ApplicantSelection.applicant_id == applicant_id
    ).order_by(
        ApplicantSelection.selection_date,
        ApplicantSelection.id
    )
    selection = db.scalars(query)
    return list(selection)

def create_selection(db: Session, applicant_id: int, data: SelectionCreate) -> ApplicantSelection | None:
    applicant = db.get(Applicant, applicant_id)
    if applicant is None:
        return None

    selection = ApplicantSelection(
        applicant_id=applicant_id,
        stage=data.stage,
        selection_date=data.selection_date,
        result=data.result,
        notes=data.notes
    )

    db.add(selection)
    db.commit()
    db.refresh(selection)
    return selection