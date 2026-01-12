# Training Project Deliverables: Authentication & Rate Limiting Implementation

## Project Description

This document describes the implementation of authentication mechanisms (API Keys and OAuth) and rate limiting for a FastAPI-based AI Chat Service. The implementation provides secure access control and protection against API abuse.

---

## 1. What Was Done

### 1.1 Authentication Mechanisms

#### API Key Authentication
- **Implementation**: Custom API key authentication system using FastAPI's `APIKeyHeader` security scheme
- **Location**: `app/core/api_key_auth.py`
- **Features**:
  - API keys stored in configuration (configurable via environment variables)
  - Header-based authentication using `X-API-Key` header
  - User identification mapping (API key → user ID)
  - Proper HTTP 401 responses with `WWW-Authenticate` headers
- **Usage**: Clients send API key in `X-API-Key` header
- **Test Coverage**: Comprehensive unit tests in `test/test_api_key_auth.py`

#### OAuth2 Authentication
- **Implementation**: OAuth2 Authorization Code flow with Bearer token support
- **Location**: `app/core/oauth.py`, `app/api/v1/auth.py`
- **Features**:
  - OAuth2 Authorization Code Bearer scheme using `python-jose` for JWT handling
  - Three endpoints: `/login`, `/callback`, `/me`
  - Demo mode support for testing (detects placeholder OAuth URLs)
  - Bearer token verification with JWT decoding
  - Support for both JWT tokens and simple bearer tokens
- **Endpoints**:
  - `GET /api/v1/auth/login` - Initiates OAuth login flow
  - `GET /api/v1/auth/callback` - Handles OAuth callback with authorization code
  - `GET /api/v1/auth/me` - Returns current authenticated user info
- **Usage**: Clients send Bearer token in `Authorization: Bearer <token>` header
- **Test Coverage**: Unit tests in `test/test_oauth.py`

#### Unified Authentication System
- **Implementation**: Flexible authentication that supports both API Key and OAuth
- **Location**: `app/core/auth.py`
- **Features**:
  - Tries API Key authentication first, then OAuth Bearer token
  - Returns `AuthContext` object with user ID and authentication method
  - Graceful fallback between authentication methods
  - Clear error messages indicating required authentication type
- **Middleware Integration**: `app/middleware/auth_middleware.py` extracts auth info for rate limiting

### 1.2 Rate Limiting

#### Implementation Details
- **Library**: `slowapi` - FastAPI-compatible rate limiting library
- **Location**: `app/middleware/rate_limit.py`
- **Features**:
  - **Per-minute limits**: Configurable requests per minute (default: 60)
  - **Per-hour limits**: Configurable requests per hour (default: 1000)
  - **User-based limiting**: Uses authenticated user ID when available
  - **IP-based fallback**: Falls back to IP address for unauthenticated requests
  - **Response headers**: Includes rate limit information in response headers:
    - `X-RateLimit-Limit-Minute`
    - `X-RateLimit-Limit-Hour`
    - `X-RateLimit-Remaining-Minute`
    - `X-RateLimit-Remaining-Hour`
  - **HTTP 429 responses**: Returns proper `429 Too Many Requests` status code
  - **Public endpoint bypass**: Health checks and documentation endpoints are excluded
- **Storage**: In-memory storage (configurable to Redis for distributed systems)
- **Configuration**: Environment-based configuration via `app/core/config.py`
- **Test Coverage**: Comprehensive tests in `test/test_rate_limit.py`

### 1.3 Architecture & Integration

#### Middleware Stack
The application uses a carefully ordered middleware stack:
1. **AuthMiddleware** - Extracts authentication information
2. **RateLimitMiddleware** - Enforces rate limits (uses auth info from previous middleware)
3. **TracingMiddleware** - Adds request tracing for observability

#### Configuration Management
- **Location**: `app/core/config.py`
- **Features**:
  - Pydantic Settings for type-safe configuration
  - Environment variable support via `.env` file
  - Default values for development
  - Separate settings for API keys, OAuth, and rate limiting

#### Endpoint Protection
- **Protected Endpoints**: `/api/v1/chat/stream` requires authentication
- **Public Endpoints**: `/api/v1/health`, `/docs`, `/openapi.json`, `/redoc`
- **OAuth Endpoints**: `/api/v1/auth/login`, `/api/v1/auth/callback` are public

### 1.4 Testing

#### Test Suite
- **Framework**: pytest with pytest-asyncio for async support
- **Coverage**: 91% code coverage (264 statements, 25 missing)
- **Test Files**:
  - `test/test_api_key_auth.py` - API key authentication tests
  - `test/test_oauth.py` - OAuth authentication tests
  - `test/test_auth.py` - Unified authentication tests
  - `test/test_rate_limit.py` - Rate limiting middleware tests
  - `test/test_endpoints.py` - Endpoint integration tests
  - `test/test_auth_middleware.py` - Authentication middleware tests
- **CI/CD**: GitHub Actions workflow runs all tests on push/PR

### 1.5 Code Quality

#### Tools & Standards
- **Black**: Code formatting
- **Ruff**: Fast Python linter
- **isort**: Import sorting
- **mypy**: Static type checking
- **Pre-commit hooks**: Automated code quality checks
- **GitHub Actions**: CI pipeline for automated testing

---

## 2. Technical Implementation Highlights

### 2.1 Authentication Flow

#### API Key Flow
```
Client Request → X-API-Key Header → verify_api_key_value() → AuthContext → Endpoint
```

#### OAuth Flow
```
Client → /auth/login → OAuth Provider → /auth/callback → Access Token → Bearer Token → verify_oauth_token() → AuthContext → Endpoint
```

### 2.2 Rate Limiting Flow
```
Request → AuthMiddleware (extract user_id) → RateLimitMiddleware (check limits) → Endpoint → Response (with rate limit headers)
```

### 2.3 Key Design Decisions

1. **Unified Authentication**: Single `get_auth_context()` function supports both auth methods, simplifying endpoint code
2. **Middleware-based Rate Limiting**: Centralized rate limiting logic, easy to configure and maintain
3. **User-based Rate Limiting**: Authenticated users get individual rate limits, preventing one user from affecting others
4. **Configurable Limits**: Environment-based configuration allows different limits for dev/staging/production
5. **Demo Mode**: OAuth includes demo mode for testing without real OAuth provider

---

## 3. Configuration

### Environment Variables

Create a `.env` file with:

```env
# API Key Settings
API_KEY_HEADER=X-API-Key

# OAuth Settings
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret
OAUTH_AUTHORIZATION_URL=https://oauth.provider.com/authorize
OAUTH_TOKEN_URL=https://oauth.provider.com/token
OAUTH_REDIRECT_URI=http://localhost:8000/api/v1/auth/callback

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
REDIS_URL=redis://localhost:6379  # Optional, for distributed rate limiting
```

---

## 4. Usage Examples

### API Key Authentication
```bash
curl -X POST http://localhost:8000/api/v1/chat/stream \
  -H "X-API-Key: test-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### OAuth Authentication
```bash
# Step 1: Get access token (demo mode)
curl http://localhost:8000/api/v1/auth/login

# Step 2: Use Bearer token
curl -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Authorization: Bearer oauth_demo_auth_code_12345" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### Rate Limit Headers
Every response includes rate limit information:
```
X-RateLimit-Limit-Minute: 60
X-RateLimit-Limit-Hour: 1000
X-RateLimit-Remaining-Minute: 59
X-RateLimit-Remaining-Hour: 999
```

---

## 5. Project Structure

```
fastApi-llm-project/
├── app/
│   ├── core/
│   │   ├── api_key_auth.py      # API key authentication
│   │   ├── oauth.py              # OAuth authentication
│   │   ├── auth.py                # Unified authentication
│   │   └── config.py             # Configuration management
│   ├── middleware/
│   │   ├── auth_middleware.py    # Authentication middleware
│   │   └── rate_limit.py         # Rate limiting middleware
│   └── api/v1/
│       └── auth.py                # OAuth endpoints
├── test/
│   ├── test_api_key_auth.py     # API key tests
│   ├── test_oauth.py            # OAuth tests
│   ├── test_auth.py              # Unified auth tests
│   └── test_rate_limit.py        # Rate limiting tests
└── README.md                      # Project documentation
```

---

## 6. Testing Results

### Test Execution
```bash
$ poetry run pytest
========================= 48 passed in 1.81s =========================
```

### Coverage Report
```
Name                                Stmts   Miss  Cover
-----------------------------------------------------------------
app/core/api_key_auth.py               15      0   100%
app/core/auth.py                       29      4    86%
app/core/oauth.py                      25      4    84%
app/middleware/auth_middleware.py      20      0   100%
app/middleware/rate_limit.py           44      2    95%
-----------------------------------------------------------------
TOTAL                                 264     18    93%
```

---

## 7. Screenshots Guide

### Recommended Screenshots:

1. **API Documentation (Swagger UI)**
   - Navigate to: `http://localhost:8000/docs`
   - Show: Authentication endpoints and chat endpoint with "Authorize" button

2. **Successful API Key Authentication**
   - Use Postman/curl/Thunder Client
   - Show: Request with `X-API-Key` header and successful 200 response

3. **Successful OAuth Authentication**
   - Show: OAuth login flow → callback → token response

4. **Rate Limit Headers in Response**
   - Show: Response headers showing `X-RateLimit-*` values

5. **Rate Limit Exceeded (429 Error)**
   - Make multiple rapid requests
   - Show: HTTP 429 response with rate limit error message

6. **Test Results**
   - Run: `poetry run pytest --cov=app --cov-report=html`
   - Show: Test results and coverage report

7. **Code Structure**
   - Show: VS Code file explorer with project structure
   - Highlight: `app/core/`, `app/middleware/`, `test/` directories

---

## 8. Reflection

*[See REFLECTION.md for the reflection paragraph]*

---

## 9. GitHub Repository

**Repository URL**: `https://github.com/ObaidaExperts/fastApi-llm-project`

**Branch**: `feature/authentication-and-rate-limiting`

**Key Commits**:
- Initial authentication implementation
- Rate limiting middleware
- Unified authentication system
- Comprehensive test suite
- Demo mode for OAuth

---

## 10. Future Enhancements

1. **Redis Integration**: Implement Redis-backed rate limiting for distributed systems
2. **Token Refresh**: Add OAuth token refresh mechanism
3. **API Key Management**: Admin endpoints for API key CRUD operations
4. **Rate Limit Policies**: Different rate limits per endpoint or user tier
5. **Monitoring**: Integration with monitoring tools (Prometheus, Grafana)
6. **Audit Logging**: Log all authentication attempts and rate limit violations

---

## Conclusion

This implementation provides a robust, production-ready authentication and rate limiting system for FastAPI applications. The code follows best practices, includes comprehensive testing, and is well-documented for maintainability.
