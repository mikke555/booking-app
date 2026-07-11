from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.config import settings
from app.exceptions import InvalidTokenError

password_hash = PasswordHash.recommended()

# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.jwt_exp)
    payload = {"sub": str(user_id), "exp": expires_at}

    return jwt.encode(
        payload,
        key=settings.jwt_key.get_secret_value(),
        algorithm=settings.jwt_alg,
    )


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            key=settings.jwt_key.get_secret_value(),
            algorithms=[settings.jwt_alg],
            options={"require": ["exp", "sub"]},
        )
        return int(payload["sub"])

    except jwt.InvalidTokenError, ValueError:
        raise InvalidTokenError
