from datetime import date
from decimal import Decimal
from typing import Self
from pydantic import BaseModel, ConfigDict, Field, model_validator

class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    full_name: str = Field(min_length=1)
    job_id: int = Field(gt=0)
    work_area_id: int = Field(gt=0)
    start_date: date
    employment_status: str = Field(min_length=1)
    base_salary: Decimal = Field(gt=0)
    manager_id: str | None = Field(default=None, min_length=1)
    applicant_id: int | None = Field(default=None, gt=0)
    work_email: str | None = None
    phone: str | None = None
    end_date: date | None = None
    tax_number: str | None = None
    tax_allowance_status: str | None = None
    bank_account_number: str | None = None
    profile_photo_url: str | None = None

    @model_validator(mode="after")
    def check_end_date(self) -> Self:
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("End date must be on or after start date.")
        return self    

class EmployeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    job_id: int
    work_area_id: int
    employment_status: str

class WorkAreaCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    city: str = Field(min_length=1)
    location_type: str = Field(min_length=1)

class WorkAreaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str
    location_type: str 