from pydantic import BaseModel, ConfigDict, Field

class ApplicantCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    job_id: int = Field(gt=0)
    full_name: str = Field(min_length=1)
    contact: str = Field(min_length=1)
    application_status: str = Field(min_length=1)

class ApplicantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: int
    full_name: str
    contact: str
    application_status: str