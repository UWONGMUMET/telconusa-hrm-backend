from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.auth.tokens import read_user_id
from db.session import get_db
from modules.access.models import User

bearer = HTTPBearer(auto_error=False)

def unauthorized() -> HTTPException:
    return HTTPException(
        status_code=401,
        detail="Invalid login or token",
        headers={"WWW-Authenticate": "Bearer"}
    )

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db)
) -> User:
    if credentials is None:
        raise unauthorized()

    user_id = read_user_id(credentials.credentials)
    if user_id is None:
        raise unauthorized()

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise unauthorized()

    return user