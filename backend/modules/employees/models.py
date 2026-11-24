from datetime import date
from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base

class WorkArea(Base):
    __tablename__= "work_areas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(Text)
    location_type: Mapped[str] = mapped_column(Text)

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    work_area_id: Mapped[int] = mapped_column(ForeignKey("work_areas.id"))
    manager_id: Mapped[str | None] = mapped_column(ForeignKey("employees.id"))
    applicant_id: Mapped[int | None] = mapped_column(
        ForeignKey("applicants.id"),
        unique=True
    )
    full_name: Mapped[str] = mapped_column(Text)
    work_email: Mapped[str | None] = mapped_column(Text, unique=True)
    phone: Mapped[str | None] = mapped_column(Text)
    start_date: Mapped[date]
    end_date: Mapped[date | None]
    employment_status: Mapped[str] = mapped_column(Text)
    base_salary: Mapped[Decimal] = mapped_column(Numeric)
    tax_number: Mapped[str | None] = mapped_column(Text)
    tax_allowance_status: Mapped[str | None] = mapped_column(Text)
    bank_account_number: Mapped[str | None] = mapped_column(Text)
    profile_photo_url: Mapped[str | None] = mapped_column(Text)