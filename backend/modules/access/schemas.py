from pydantic import BaseModel, ConfigDict, Field, SecretStr

class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: SecretStr

class UserCreate(LoginRequest):
    employee_id: str = Field(min_length=1)

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: str
    username: str
    is_active: bool

class UserProfile(UserRead):
    roles: list[str]

class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"