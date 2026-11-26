from datetime import date
from typing import Self
from pydantic import BaseModel, ConfigDict, Field, model_validator

class ContractCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    contract_type: str = Field(min_length=1)
    start_date: date
    end_date: date | None = None
    document_url: str | None = None

    @model_validator(mode="after")
    def check_end_date(self) -> Self:
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("End date must be on or after start date")
        return self

class ContractRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: str
    contract_type: str
    start_date: date
    end_date: date | None
    document_url: str | None

class OnboardingCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    start_date: date
    status: str = Field(min_length=1)
    completed_date: date | None = None

    @model_validator(mode="after")
    def check_completed_date(self) -> Self:
        if self.completed_date and self.completed_date < self.start_date:
            raise ValueError("Completed date must be on or after start date")
        return self

class OnboardingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: str
    start_date: date
    status: str
    completed_date: date | None

class OffboardingCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    request_date: date
    effective_date: date
    reason: str = Field(min_length=1)
    status: str = Field(min_length=1)

class OffBoardingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    employee_id: str
    request_date: date
    effective_date: date 
    reason: str 
    status: str