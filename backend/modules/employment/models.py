from datetime import date
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

class EmploymentContract(Base):
    __tablename__ = "employment_contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"))
    contract_type: Mapped[str] = mapped_column(Text)
    start_date: Mapped[date]
    end_date: Mapped[date | None]
    document_url: Mapped[str | None] = mapped_column(Text)

class Onboarding(Base):
    __tablename__ = "onboarding"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"))
    start_date: Mapped[date]
    status: Mapped[str] = mapped_column(Text)
    completed_date: Mapped[str | None]

class Offboarding(Base):
    __tablename__ = "offboarding"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"))
    request_date: Mapped[date]
    effective_date: Mapped[date]
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)