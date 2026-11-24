from decimal import Decimal
from sqlalchemy import Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base

class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    cost_center_code: Mapped[str] = mapped_column(Text, unique=True)

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    name: Mapped[str] = mapped_column(Text)
    allowance: Mapped[Decimal] = mapped_column(Numeric)