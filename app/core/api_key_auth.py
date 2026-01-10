from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER, auto_error=False)


def verify_api_key_value(api_key: str):
    """
    Verify API key value directly (for use in unified auth).
    Returns user_id if valid, raises HTTPException if invalid.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    user_id = settings.API_KEYS.get(api_key)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return user_id


async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verify API key from header using FastAPI Security dependency.
    Returns AuthContext if valid, raises HTTPException if invalid.
    """
    from app.core.auth import AuthContext

    user_id = verify_api_key_value(api_key)
    return AuthContext(user_id=user_id)
