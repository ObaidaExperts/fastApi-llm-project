from fastapi import Header, HTTPException, status

from app.core.oauth import verify_bearer_token


class AuthContext:
    def __init__(self, user_id: str, auth_method: str = "unknown"):
        self.user_id = user_id
        self.auth_method = auth_method


async def get_auth_context(
    api_key: str | None = Header(default=None, alias="X-API-Key"),
    authorization: str | None = Header(default=None),
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
            auth_context_result: AuthContext = await verify_bearer_token(authorization)
            auth_context_result.auth_method = "oauth"
            return auth_context_result
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

    # Create a mock request for the security scheme
    # In practice, this should be used as a dependency with Depends()
    # For now, we'll use the direct verification approach

    # This function should be used with Depends(api_key_header) in actual endpoints
    # For standalone use, we need to get the API key differently
    raise NotImplementedError(
        "Use Depends(verify_api_key) or get_auth_context() instead of require_api_key()"
    )


async def require_oauth() -> AuthContext:
    """Dependency that requires OAuth authentication."""

    # This function should be used with Depends(oauth2_scheme) in actual endpoints
    # For standalone use, we need to get the token differently
    raise NotImplementedError(
        "Use Depends(verify_oauth_token) or get_auth_context() instead of require_oauth()"
    )
