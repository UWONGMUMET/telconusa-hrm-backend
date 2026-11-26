from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.auth.authentication import get_current_user
from db.session import get_db
from modules.access.models import User
from modules.access.services import list_roles

def require_hr_manager(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    roles = list_roles(db, user.id)
    if "hr_manager" not in roles:
        raise HTTPException(status_code=403, detail="HR manager role required")

    return user