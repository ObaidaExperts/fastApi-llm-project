from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.core.oauth import oauth2_scheme

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/login")
async def oauth_login():
    """
    Initiate OAuth login flow.
    Redirects to OAuth provider authorization URL.
    """
    auth_url = (
        f"{settings.OAUTH_AUTHORIZATION_URL}"
        f"?client_id={settings.OAUTH_CLIENT_ID}"
        f"&redirect_uri={settings.OAUTH_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=read write"
    )
    return RedirectResponse(url=auth_url)

@router.get("/callback")
async def oauth_callback(code: str):
    """
    OAuth callback endpoint.
    Exchanges authorization code for access token.
    """
    # In production, exchange code for token with OAuth provider
    # For demo purposes, return a mock token
    return {
        "access_token": f"oauth_{code}",
        "token_type": "bearer",
        "expires_in": 3600,
    }

@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get current authenticated user info.
    """
    from app.core.oauth import verify_oauth_token
    auth_context = await verify_oauth_token(token)
    return {
        "user_id": auth_context.user_id,
        "auth_method": "oauth",
    }
