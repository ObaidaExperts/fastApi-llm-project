from pydantic import BaseModel, Field


class OAuthTokenResponse(BaseModel):
    """OAuth token response model."""

    access_token: str = Field(
        ...,
        description="OAuth access token",
        examples=["oauth_demo_auth_code_12345"],
    )
    token_type: str = Field(
        ...,
        description="Token type (typically 'bearer')",
        examples=["bearer"],
        pattern="^bearer$",
    )
    expires_in: int = Field(
        ...,
        description="Token expiration time in seconds",
        examples=[3600],
        gt=0,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "access_token": "oauth_demo_auth_code_12345",
                    "token_type": "bearer",
                    "expires_in": 3600,
                }
            ]
        }
    }


class UserInfoResponse(BaseModel):
    """User information response model."""

    user_id: str = Field(
        ...,
        description="Unique identifier for the authenticated user",
        examples=["user1"],
    )
    auth_method: str = Field(
        ...,
        description="Authentication method used",
        examples=["oauth", "api_key"],
        pattern="^(oauth|api_key)$",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"user_id": "user1", "auth_method": "oauth"},
                {"user_id": "user2", "auth_method": "api_key"},
            ]
        }
    }


class OAuthCallbackQuery(BaseModel):
    """OAuth callback query parameters."""

    code: str = Field(
        ...,
        description="Authorization code from OAuth provider",
        examples=["demo_auth_code_12345"],
        min_length=1,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"code": "demo_auth_code_12345"},
            ]
        }
    }
