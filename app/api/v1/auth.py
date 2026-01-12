from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.core.oauth import oauth2_scheme
from app.models.auth import OAuthTokenResponse, UserInfoResponse

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get(
    "/login",
    summary="Initiate OAuth login",
    description="Initiates the OAuth login flow. Redirects to OAuth provider authorization URL. "
    "In demo mode, redirects directly to callback with a demo authorization code.",
    response_class=RedirectResponse,
)
async def oauth_login() -> RedirectResponse:
    """
    Initiate OAuth login flow.

    Returns:
        RedirectResponse: Redirects to OAuth provider or callback (in demo mode)
    """
    # Check if we're in demo mode (placeholder OAuth URL)
    if (
        "oauth.provider.com" in settings.OAUTH_AUTHORIZATION_URL
        or settings.OAUTH_CLIENT_ID == "your-client-id"
    ):
        # Demo mode: redirect directly to callback with a demo authorization code
        demo_code = "demo_auth_code_12345"
        callback_url = f"{settings.OAUTH_REDIRECT_URI}?code={demo_code}"
        return RedirectResponse(url=callback_url)

    # Production mode: redirect to actual OAuth provider
    auth_url = (
        f"{settings.OAUTH_AUTHORIZATION_URL}"
        f"?client_id={settings.OAUTH_CLIENT_ID}"
        f"&redirect_uri={settings.OAUTH_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=read write"
    )
    return RedirectResponse(url=auth_url)


@router.get(
    "/callback",
    response_model=OAuthTokenResponse,
    summary="OAuth callback endpoint",
    description="OAuth callback endpoint that exchanges authorization code for access token. "
    "In production, this would exchange the code with the OAuth provider.",
)
async def oauth_callback(
    code: str = Query(
        ...,
        description="Authorization code from OAuth provider",
        examples=["demo_auth_code_12345"],
    ),
) -> OAuthTokenResponse:
    """
    OAuth callback endpoint.

    Args:
        code: Authorization code from OAuth provider

    Returns:
        OAuthTokenResponse: Access token and related information
    """
    # In production, exchange code for token with OAuth provider
    # For demo purposes, return a mock token
    return OAuthTokenResponse(
        access_token=f"oauth_{code}",
        token_type="bearer",
        expires_in=3600,
    )


@router.get(
    "/me",
    response_model=UserInfoResponse,
    summary="Get current user info",
    description="Returns information about the currently authenticated user.",
)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> UserInfoResponse:
    """
    Get current authenticated user info.

    Args:
        token: OAuth bearer token from Authorization header

    Returns:
        UserInfoResponse: User ID and authentication method
    """
    from app.core.oauth import verify_oauth_token

    auth_context = await verify_oauth_token(token)
    return UserInfoResponse(
        user_id=auth_context.user_id,
        auth_method="oauth",
    )
