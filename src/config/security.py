from typing import MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi import Header, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from starlette import status

from src.config.config import settings

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(*, sub: str, username: str, registration_number: int) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
        username=username,
        registration_number=registration_number
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
    username: str,
    registration_number: int
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    payload["iat"] = datetime.utcnow()

    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    payload["sub"] = sub

    payload["username"] = username
    payload["registration_number"] = registration_number

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def decode_token(encoded_token: str):
    try:
        decoded_token = jwt.decode(encoded_token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return decoded_token
    except Exception:
        return {}


def verify_jwt(token: str = Header(...)) -> None:
    authorized = bool(decode_token(token))
    if not authorized:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_token(
    token: str = Depends(oauth2_scheme)
) -> List[str]:
    payload = decode_token(token)
    return payload.get("permissions")


def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> dict:
    payload = decode_token(token)
    return {
        "token": token,
        "registration_number": payload.get("registration_number")
    }
