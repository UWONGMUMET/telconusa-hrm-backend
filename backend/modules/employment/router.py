from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from modules.employment import services
from modules.employment.schemas import (
    ContractCreate,
    ContractRead,
    OnboardingCreate,
    OnboardingRead,
    OffboardingCreate,
    OffBoardingRead
)

router = APIRouter(prefix="/employees", tags=["employments"])
Database = Annotated[Session, Depends(get_db)]

@router.get("/{employee_id}/contracts", response_model=list[ContractRead])
def list_contracts(employee_id: str, db: Database):
    contracts = services.list_contracts(db, employee_id)
    if contracts is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return contracts

@router.post("/{employee_id}/contracts", response_model=ContractRead, status_code=201)
def create_selection(employee_id: str, data: ContractCreate, db: Database):
    contracts = services.create_contract(db, employee_id, data)
    if contracts is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return contracts

@router.get("/{employee_id}/onboarding", response_model=list[OnboardingRead])
def list_onboardings(employee_id: str, db: Database):
    onboarding = services.list_oboardings(db, employee_id)
    if onboarding is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return onboarding

@router.post("/{employee_id}/onboarding", response_model=OnboardingRead, status_code=201)
def create_onboarding(employee_id: str, data: OnboardingCreate, db: Database):
    onboarding = services.create_onboarding(db, employee_id, data)
    if onboarding is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return onboarding

@router.get("/{employee_id}/offboarding", response_model=list[OffBoardingRead])
def list_offboardings(employee_id: str, db: Database):
    offboarding = services.list_offboardings(db, employee_id)
    if offboarding is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return offboarding

@router.post("/{employee_id}/offboarding", response_model=OffboardingCreate, status_code=201)
def create_offboarding(employee_id: str, data: OffboardingCreate, db: Database):
    offboarding = services.create_offboarding(db, employee_id, data)
    if offboarding is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return offboarding 