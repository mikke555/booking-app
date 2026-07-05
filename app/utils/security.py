from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.config import settings
from app.exceptions import InvalidToken

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.jwt_exp)
    payload = {"sub": str(user_id), "exp": expires_at}

    return jwt.encode(payload, key=settings.jwt_key, algorithm=settings.jwt_alg)


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            key=settings.jwt_key,
            algorithms=[settings.jwt_alg],
            options={"require": ["exp", "sub"]},
        )
        return int(payload["sub"])

    except jwt.InvalidTokenError, ValueError:
        raise InvalidToken
