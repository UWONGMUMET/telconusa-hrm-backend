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