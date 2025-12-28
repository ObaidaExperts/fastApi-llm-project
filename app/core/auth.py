from fastapi import Depends, Header

class AuthContext:
    def __init__(self, user_id: str):
        self.user_id = user_id

def get_auth_context(
    authorization: str | None = Header(default=None),
) -> AuthContext:
    # Simplified example
    user_id = authorization or "anonymous"
    return AuthContext(user_id=user_id)
