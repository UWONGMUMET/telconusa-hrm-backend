from datetime import date
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

class Applicant(Base):
    __tablename__ = "applicants"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    full_name: Mapped[str] = mapped_column(Text)
    contact: Mapped[str] = mapped_column(Text)
    application_status: Mapped[str] = mapped_column(Text)

class ApplicantSelection(Base):
    __tablename__ = "applicant_selections"

    id: Mapped[int] = mapped_column(primary_key=True)
    applicant_id: Mapped[int] = mapped_column(ForeignKey("applicants.id"))
    stage: Mapped[str] = mapped_column(Text)
    selection_date: Mapped[date]
    result: Mapped[str] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)