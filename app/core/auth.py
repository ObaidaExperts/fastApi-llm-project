from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from app.core.oauth import verify_bearer_token

class AuthContext:
    def __init__(self, user_id: str, auth_method: str = "unknown"):
        self.user_id = user_id
        self.auth_method = auth_method

async def get_auth_context(
    api_key: Optional[str] = Header(default=None, alias="X-API-Key"),
    authorization: Optional[str] = Header(default=None),
) -> AuthContext:
    """
    Unified authentication that supports both API Key and OAuth.
    Tries API Key first, then OAuth Bearer token.
    """
    # Try API Key authentication first
    if api_key:
        try:
            from app.core.api_key_auth import verify_api_key_value
            user_id = verify_api_key_value(api_key)
            auth_context = AuthContext(user_id=user_id, auth_method="api_key")
            return auth_context
        except HTTPException:
            pass
    
    # Try OAuth Bearer token authentication
    if authorization and authorization.startswith("Bearer "):
        try:
            auth_context = await verify_bearer_token(authorization)
            auth_context.auth_method = "oauth"
            return auth_context
        except HTTPException:
            pass
    
    # If neither works, raise authentication error
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Provide either API Key (X-API-Key header) or Bearer token (Authorization header)",
        headers={"WWW-Authenticate": "ApiKey, Bearer"},
    )

# Separate dependencies for explicit auth method selection
async def require_api_key() -> AuthContext:
    """Dependency that requires API key authentication."""
    from fastapi import Security
    from app.core.api_key_auth import api_key_header, verify_api_key
    return await verify_api_key(await api_key_header())

async def require_oauth() -> AuthContext:
    """Dependency that requires OAuth authentication."""
    from fastapi import Depends
    from app.core.oauth import oauth2_scheme, verify_oauth_token
    return await verify_oauth_token(await oauth2_scheme())
