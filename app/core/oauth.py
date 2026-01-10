from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt

from app.core.config import settings

# OAuth2 scheme
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.OAUTH_AUTHORIZATION_URL,
    tokenUrl=settings.OAUTH_TOKEN_URL,
    scopes={"read": "Read access", "write": "Write access"},
)


async def verify_oauth_token(token: str = Depends(oauth2_scheme)):
    """
    Verify OAuth2 bearer token.
    Returns AuthContext if valid, raises HTTPException if invalid.
    """
    from app.core.auth import AuthContext

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token (adjust based on your OAuth provider)
        payload = jwt.decode(
            token,
            settings.OAUTH_CLIENT_SECRET,
            algorithms=["HS256"],
            options={"verify_signature": False},  # For demo - use proper verification in production
        )
        user_id: str = payload.get("sub") or payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError as err:
        raise credentials_exception from err

    return AuthContext(user_id=user_id)


# Alternative: Simple bearer token verification (for non-JWT tokens)
async def verify_bearer_token(authorization: str | None = None):
    """
    Simple bearer token verification (for demonstration).
    In production, validate against your OAuth provider.
    """
    from app.core.auth import AuthContext

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.replace("Bearer ", "")
    # In production, validate token with OAuth provider
    # For demo, accept any token starting with "oauth_"
    if token.startswith("oauth_"):
        user_id = token.replace("oauth_", "user_")
        return AuthContext(user_id=user_id)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid bearer token",
        headers={"WWW-Authenticate": "Bearer"},
    )
