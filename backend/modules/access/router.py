from fastapi import APIRouter, Depends, HTTPException
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.auth.authentication import get_current_user, unauthorized
from core.auth.authorization import require_hr_manager
from core.auth.tokens import create_token
from db.session import get_db
from modules.access import services
from modules.access.models import User
from modules.access.schemas import (
    LoginRequest,
    RoleRead,
    TokenResponse,
    UserCreate,
    UserProfile,
    UserRead
)
from modules.employees.models import Employee

router = APIRouter(tags=["access"])

@router.post("/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    password = data.password.get_secret_value()
    user = services.authenticate_user(db, data.username, password)
    if user is None:
        raise unauthorized()

    return TokenResponse(access_token=create_token(user.id))

@router.get("/auth/me", response_model=UserProfile)
def get_me(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return UserProfile(
        id=user.id,
        employee_id=user.employee_id,
        username=user.username,
        is_active=user.is_active,
        roles=services.list_roles(db, user.id)
    )

@router.get(
    "/access/users",
    response_model=list[UserRead],
    dependencies=[Depends(require_hr_manager)]
)
def list_users(db: Session = Depends(get_db)):
    return services.list_users(db)

@router.get(
    "/access/roles",
    response_model=list[RoleRead],
    dependencies=[Depends(require_hr_manager)]
)
def list_roles(db: Session = Depends(get_db)):
    return services.list_all_roles(db)

@router.post(
    "/access/users",
    response_model=UserRead,
    status_code=201,
    dependencies=[Depends(require_hr_manager)]
)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    if db.get(Employee, data.employee_id) is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    role = services.get_role(db, "employee")
    if role is None:
        raise HTTPException(status_code=503, detail="Employee role is missing")

    try:
        return services.create_user(db, data, role)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except IntegrityError as error:
        if isinstance(error.orig, UniqueViolation):
            raise HTTPException(
                status_code=409,
                detail="Username or employee account already exists"
            ) from error
        raise