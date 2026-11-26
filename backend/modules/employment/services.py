from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.employees.models import Employee
from modules.employment.models import EmploymentContract, Onboarding, Offboarding
from modules.employment.schemas import ContractCreate, OnboardingCreate, OffboardingCreate

def list_contracts(db: Session, employee_id: str) -> list[EmploymentContract] | None:
    employee = db.get(Employee, employee_id)
    if employee is None:
        return None

    query = select(EmploymentContract).where(
        EmploymentContract.employee_id == employee_id
    ).order_by(
        EmploymentContract.start_date,
        EmploymentContract.id
    )

    employment = db.scalars(query)
    return list(employment)

def create_contract(db: Session, employee_id: str, data: ContractCreate) -> EmploymentContract | None:
    employee = db.get(Employee, employee_id)
    if employee is None:
        return None

    contract = EmploymentContract(
        employee_id=employee_id,
        contract_type=data.contract_type,
        start_date=data.start_date,
        end_date=data.end_date,
        document_url=data.document_url
    )

    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract

def list_onboardings(db: Session, employee_id: str) -> list[Onboarding] | None:
    employee = db.get(Employee, employee_id)
    if employee is None:
        return None

    query = select(Onboarding).where(
        Onboarding.employee_id == employee_id
    ).order_by(
        Onboarding.start_date,
        Onboarding.id
    )

    onboarding = db.scalars(query)
    return list(onboarding)

def create_onboarding(db: Session, employee_id: str, data: OnboardingCreate) -> Onboarding | None:
    employee = db.get(Employee, employee_id)
    if employee is None:
        return None

    onboarding = Onboarding(
        employee_id=employee_id,
        start_date=data.start_date,
        status=data.status,
        completed_date=data.completed_date
    )

    db.add(onboarding)
    db.commit()
    db.refresh(onboarding)
    return onboarding

def list_offboardings(db: Session, employee_id: str) -> list[Offboarding] | None:
    employee = db.get(Employee, employee_id)
    if employee is None:
        return None

    query = select(Offboarding).where(
        Offboarding.employee_id == employee_id
    ).order_by(
        Offboarding.request_date,
        Offboarding.id
    )

    offboardig = db.scalars(query)
    return list(offboardig)

def create_offboarding(db: Session, employee_id: str, data: OffboardingCreate) -> Offboarding | None:
    employee = db.get(Employee, employee_id)
    if employee is None:
        return None

    offboarding = Offboarding(
        employee_id=employee_id,
        request_date=data.request_date,
        effective_date=data.effective_date,
        reason=data.reason,
        status=data.status
    )

    db.add(offboarding)
    db.commit()
    db.refresh(offboarding)
    return offboarding