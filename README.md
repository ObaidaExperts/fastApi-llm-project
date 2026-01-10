# FastAPI LLM Project

A FastAPI-based AI Chat Service with streaming support for Large Language Model (LLM) interactions.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 💬 **Streaming Chat** - Server-sent events (SSE) for real-time chat responses
- 🔐 **Authentication** - API key and OAuth2 authentication support
- 🛡️ **Rate Limiting** - Per-minute and per-hour rate limiting
- 🔄 **Health Check** - Service health monitoring endpoint
- 🐳 **Docker Support** - DevContainer configuration for easy development
- 📦 **Type Safety** - Pydantic models for request/response validation
- ✅ **Testing** - Comprehensive unit test suite

## Project Structure

```
fastApi-llm-project/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── chat.py          # Chat streaming endpoint
│   │   │   ├── health.py        # Health check endpoint
│   │   │   ├── auth.py          # OAuth endpoints
│   │   │   └── router.py        # API v1 router
│   │   └── router.py            # Main API router
│   ├── core/
│   │   ├── auth.py              # Unified authentication
│   │   ├── api_key_auth.py      # API key authentication
│   │   ├── oauth.py             # OAuth authentication
│   │   ├── config.py            # Application configuration
│   │   ├── database.py          # Database session
│   │   └── tracing.py           # Tracing utilities
│   ├── middleware/
│   │   ├── auth_middleware.py   # Authentication middleware
│   │   ├── rate_limit.py        # Rate limiting middleware
│   │   └── tracing.py           # Tracing middleware
│   ├── models/
│   │   ├── chat.py              # Chat request/response models
│   │   └── health.py            # Health check models
│   ├── services/
│   │   └── chat_service.py      # Chat streaming service logic
│   └── main.py                  # FastAPI application entry point
├── test/
│   ├── test_api_key_auth.py     # API key auth tests
│   ├── test_oauth.py            # OAuth tests
│   ├── test_auth.py              # Unified auth tests
│   ├── test_rate_limit.py        # Rate limiting tests
│   ├── test_endpoints.py         # Endpoint tests
│   └── conftest.py              # Pytest fixtures
├── docs/
│   ├── TESTING.md                # Testing guide
│   └── IMPLEMENTATION_SUMMARY.md # Implementation documentation
├── .devcontainer/
│   ├── Dockerfile               # Development container image
│   └── devcontainer.json        # VS Code devcontainer configuration
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
└── README.md                    # This file
```

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ObaidaExperts/fastApi-llm-project.git
cd fastApi-llm-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Health Check
```http
GET /api/v1/health
```

Response:
```json
{
  "status": "ok",
  "trace_id": "uuid-here"
}
```

#### Chat Stream (Requires Authentication)
```http
POST /api/v1/chat/stream
X-API-Key: your-api-key
Content-Type: application/json
```

Or with OAuth:
```http
POST /api/v1/chat/stream
Authorization: Bearer your-oauth-token
Content-Type: application/json
```

Request Body:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello, how are you?"
    }
  ]
}
```

Response: Server-Sent Events (SSE) stream
```
data: {"token": "Hello", "trace_id": "...", "finished": false}
data: {"token": "how", "trace_id": "...", "finished": false}
data: {"token": "", "trace_id": "...", "finished": true}
```

#### OAuth Endpoints
- `GET /api/v1/auth/login` - Initiate OAuth login
- `GET /api/v1/auth/callback` - OAuth callback
- `GET /api/v1/auth/me` - Get current user info

### Example Usage with cURL

```bash
# Health check (no auth required)
curl http://localhost:8000/api/v1/health

# Chat stream with API key
curl -X POST http://localhost:8000/api/v1/chat/stream \
  -H "X-API-Key: test-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Tell me a joke"}
    ]
  }'

# Chat stream with OAuth token
curl -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Authorization: Bearer oauth_test123" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }'
```

See `docs/TESTING.md` for more examples.

## Development

### Using DevContainer

This project includes a VS Code DevContainer configuration for a consistent development environment:

1. Open the project in VS Code
2. When prompted, click "Reopen in Container"
3. The container will automatically:
   - Install dependencies
   - Start the FastAPI server on port 8000
   - Configure Python extensions

### Running Tests

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest test/test_api_key_auth.py
```

See `test/README.md` for more testing information.

### Environment Variables

Create a `.env` file in the project root for environment-specific configuration:

```env
# API Key Settings
API_KEY_HEADER=X-API-Key

# OAuth Settings
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

See `docs/IMPLEMENTATION_SUMMARY.md` for detailed configuration options.

## Documentation

- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)** - Detailed documentation of authentication and rate limiting implementation
- **[Testing Guide](docs/TESTING.md)** - Manual testing instructions and examples
- **[Test Suite](test/README.md)** - Unit test documentation

## Dependencies

### Core Dependencies
- **fastapi** >= 0.110 - Web framework
- **uvicorn[standard]** >= 0.27 - ASGI server
- **pydantic** >= 2.0 - Data validation
- **pydantic-settings** >= 2.0.0 - Configuration management

### Authentication & Security
- **python-jose[cryptography]** >= 3.3.0 - JWT token handling
- **python-multipart** >= 0.0.6 - Form data support

### Rate Limiting
- **slowapi** >= 0.1.9 - Rate limiting library
- **redis** >= 5.0.0 - Optional Redis support for distributed rate limiting

### Testing
- **pytest** >= 7.4.0 - Testing framework
- **pytest-asyncio** >= 0.21.0 - Async test support
- **pytest-cov** >= 4.1.0 - Coverage reporting

## Next Steps

To integrate with a real LLM provider:

1. Update `app/services/chat_service.py` to connect to your LLM API
2. Add API keys to your `.env` file
3. Update `app/core/config.py` to load configuration from environment variables

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
