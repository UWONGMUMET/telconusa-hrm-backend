from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class DepartmentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    cost_center_code: str = Field(min_length=1)

class DepartmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    cost_center_code: str

class JobCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    department_id: int = Field(gt=0)
    name: str = Field(min_length=1)
    allowance: Decimal = Field(ge=0)

class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    department_id: int
    name: str
    allowance: Decimal