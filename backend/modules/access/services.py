from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.auth.passwords import hash_password, verify_password
from modules.access.models import Role, User, UserRole
from modules.access.schemas import UserCreate

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    query = select(User).where(User.username == username)
    user = db.scalar(query)
    if user is None:
        verify_password(password, None)
        return None

    if not verify_password(password, user.password_hash):
        return None

    if not user.is_active:
        return None

    return user

def get_role(db: Session, name: str) -> Role | None:
    query = select(Role).where(Role.name == name)
    return db.scalar(query)

def list_roles(db: Session, user_id: int) -> list[str]:
    query = (
        select(Role.name).join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id).order_by(Role.name)
    )
    return list(db.scalars(query))

def list_all_roles(db: Session) -> list[Role]:
    return list(db.scalars(select(Role).order_by(Role.name)))

def list_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.id)))

def create_user(db: Session, data: UserCreate, role: Role) -> User:
    password = data.password.get_secret_value()
    if len(password) < 8 or len(password) > 1024:
        raise ValueError("Password must have between 8 and 1024 characters")

    user = User(
        employee_id=data.employee_id,
        username=data.username,
        password_hash=hash_password(password),
        is_active=True,
    )

    try:
        db.add(user)
        db.flush()
        db.add(UserRole(user_id=user.id, role_id=role.id))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(user)
    return user