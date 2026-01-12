from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API Key Settings
    API_KEY_HEADER: str = "X-API-Key"
    API_KEYS: dict[str, str] = {
        "test-api-key-123": "user1",
        "test-api-key-456": "user2",
    }

    # OAuth Settings
    OAUTH_CLIENT_ID: str = "your-client-id"
    OAUTH_CLIENT_SECRET: str = "your-client-secret"
    OAUTH_AUTHORIZATION_URL: str = "https://oauth.provider.com/authorize"
    OAUTH_TOKEN_URL: str = "https://oauth.provider.com/token"
    OAUTH_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/callback"

    # Rate Limiting Settings
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    REDIS_URL: str | None = None  # Optional: "redis://localhost:6379"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
