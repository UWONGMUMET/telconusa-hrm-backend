from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from modules.recruitment import services
from modules.recruitment.schemas import (
    ApplicantCreate, 
    ApplicantRead,
    SelectionCreate,
    SelectionRead
)

router = APIRouter(prefix="/applicants", tags=["applicants"])
Database = Annotated[Session, Depends(get_db)]

@router.get("", response_model=list[ApplicantRead])
def list_applicants(db: Database):
    return services.list_applicants(db)

@router.post("", response_model=ApplicantRead, status_code=201)
def create_applicant(data: ApplicantCreate, db: Database):
    applicant = services.create_applicant(db, data)
    if applicant is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return applicant

@router.get("/{applicant_id}/selections", response_model=list[SelectionRead])
def list_selections(applicant_id: int, db: Database):
    selections = services.list_selection(db, applicant_id)
    if selections is None:
        raise HTTPException(status_code=404, detail="Applicant not found")

    return selections

@router.post("/{applicant_id}/selections", response_model=SelectionRead, status_code=201)
def create_selection(applicant_id: int, data: SelectionCreate, db: Database):
    selections = services.create_selection(db, applicant_id, data)
    if selections is None:
        raise HTTPException(status_code=404, detail="Applicant not found")
    
    return selections