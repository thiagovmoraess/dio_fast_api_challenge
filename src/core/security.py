from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from src.core.config import settings

password_hasher = PasswordHash.recommended()


class InvalidTokenException(Exception):
    pass


def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.jwt_expire_minutes)

    payload = {"sub": subject, "iat": now, "exp": expire}

    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, any]:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.InvalidTokenError as exc:
        raise InvalidTokenException("Invalid token") from exc

    sub = payload.get("sub")

    if not sub:
        raise InvalidTokenException("Invalid token: missing subject")

    if not isinstance(sub, str):
        raise InvalidTokenException("Invalid token: subject must be a string")

    return payload
