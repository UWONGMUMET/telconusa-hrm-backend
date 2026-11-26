from datetime import UTC, datetime, timedelta
import jwt

from core.config import Settings

secret = Settings().jwt_secret.get_secret_value()

def create_token(user_id: int) -> str:
    claims = {
        "sub": str(user_id),
        "exp": datetime.now(UTC) + timedelta(minutes=30)
    }
    return jwt.encode(claims, secret, algorithm="HS256")

def read_user_id(token: str) -> int | None:
    try:
        claims = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            options={"require": ["sub", "exp"]}
        )
        return int(claims["sub"])
    except (jwt.InvalidTokenError, ValueError):
        return None