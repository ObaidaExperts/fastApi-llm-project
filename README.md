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
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI pipeline
├── docs/
│   ├── TESTING.md                # Testing guide
│   └── IMPLEMENTATION_SUMMARY.md # Implementation documentation
├── test/
│   ├── test_api_key_auth.py     # API key auth tests
│   ├── test_oauth.py            # OAuth tests
│   ├── test_auth.py              # Unified auth tests
│   ├── test_rate_limit.py        # Rate limiting tests
│   ├── test_endpoints.py         # Endpoint tests
│   └── conftest.py              # Pytest fixtures
├── .python-version              # Python version for pyenv
├── pyproject.toml               # Poetry configuration and dependencies
├── Makefile                     # Developer convenience commands
├── .pre-commit-config.yaml      # Pre-commit hooks configuration
├── requirements.txt             # Legacy pip dependencies (use Poetry instead)
├── pytest.ini                   # Pytest configuration (also in pyproject.toml)
└── README.md                    # This file
```

## Installation

### Prerequisites

- **Python 3.11+** (managed via pyenv)
- **Poetry** (dependency management)
- **Make** (optional, for convenience commands)

### Setup with Poetry (Recommended)

1. **Install pyenv** (if not already installed):
```bash
# macOS
brew install pyenv

# Linux
curl https://pyenv.run | bash
```

2. **Install Python 3.11.14**:
```bash
pyenv install 3.11.14
pyenv local 3.11.14  # Sets Python version for this project
```

3. **Install Poetry**:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

4. **Clone the repository**:
```bash
git clone https://github.com/ObaidaExperts/fastApi-llm-project.git
cd fastApi-llm-project
```

5. **Install dependencies**:
```bash
# Install all dependencies (including dev dependencies)
make install-dev

# Or using Poetry directly
poetry install
```

### Alternative: Using requirements.txt (Legacy)

If you prefer pip:
```bash
pip install -r requirements.txt
```

**Note:** Poetry is the recommended approach for this project.

## Usage

### Running the Application

**Using Make (Recommended)**:
```bash
make run
```

**Using Poetry**:
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Direct uvicorn** (if dependencies installed via pip):
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

### Using DevContainer (Recommended)

This project includes a VS Code DevContainer configuration with Poetry pre-installed:

1. Open the project in VS Code
2. When prompted, click "Reopen in Container"
3. The container will automatically:
   - Install Poetry and dependencies
   - Set up pre-commit hooks
   - Start the FastAPI server on port 8000
   - Configure Python extensions (Black, Ruff, Pylance)

### Makefile Commands

This project includes a `Makefile` with convenient commands:

```bash
make help          # Show all available commands
make install       # Install production dependencies
make install-dev   # Install all dependencies (including dev)
make run           # Run the FastAPI application
make test          # Run tests
make test-cov      # Run tests with coverage report
make lint          # Run linting checks (ruff)
make lint-fix      # Fix linting issues automatically
make format        # Format code (black + isort)
make format-check  # Check formatting without changes
make type-check    # Run type checking (mypy)
make precommit     # Run all pre-commit checks
make clean         # Clean cache files and build artifacts
```

### Running Tests

**Using Make**:
```bash
make test          # Run all tests
make test-cov      # Run with coverage report
```

**Using Poetry**:
```bash
poetry run pytest                    # Run all tests
poetry run pytest --cov=app          # Run with coverage
poetry run pytest test/test_auth.py  # Run specific test file
```

**Direct pytest** (if dependencies installed via pip):
```bash
pytest
pytest --cov=app --cov-report=html
```

See `test/README.md` for more testing information.

### Code Quality

#### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality:

```bash
# Install pre-commit hooks (automatically done in DevContainer)
poetry run pre-commit install

# Run hooks manually
make precommit

# Or using pre-commit directly
poetry run pre-commit run --all-files
```

Hooks include:
- **Black** - Code formatting
- **Ruff** - Fast Python linter
- **isort** - Import sorting
- **mypy** - Type checking
- **Trailing whitespace** - Remove trailing whitespace
- **End of file fixer** - Ensure files end with newline

#### Manual Code Quality Checks

```bash
# Format code
make format

# Check formatting
make format-check

# Lint code
make lint

# Fix linting issues
make lint-fix

# Type check
make type-check
```

### CI/CD

This project includes GitHub Actions CI that runs on every push and pull request:

- **Code formatting check** (Black)
- **Import sorting check** (isort)
- **Linting** (Ruff)
- **Type checking** (mypy)
- **Tests** (pytest with coverage)

View CI status in the GitHub Actions tab of the repository.

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

Dependencies are managed via Poetry. See `pyproject.toml` for the complete list.

### Core Dependencies
- **fastapi** ^0.110.0 - Web framework
- **uvicorn[standard]** ^0.27.0 - ASGI server
- **pydantic** ^2.0.0 - Data validation
- **pydantic-settings** ^2.0.0 - Configuration management

### Authentication & Security
- **python-jose[cryptography]** ^3.3.0 - JWT token handling
- **python-multipart** ^0.0.6 - Form data support

### Rate Limiting
- **slowapi** ^0.1.9 - Rate limiting library
- **redis** ^5.0.0 - Optional Redis support for distributed rate limiting

### Development Dependencies
- **pytest** ^7.4.0 - Testing framework
- **pytest-asyncio** ^0.21.0 - Async test support
- **pytest-cov** ^4.1.0 - Coverage reporting
- **black** ^23.12.0 - Code formatter
- **ruff** ^0.1.0 - Fast Python linter
- **mypy** ^1.7.0 - Static type checker
- **isort** ^5.13.0 - Import sorter
- **pre-commit** ^3.6.0 - Git hooks framework

### Managing Dependencies

```bash
# Add a new dependency
poetry add package-name

# Add a dev dependency
poetry add --group dev package-name

# Update dependencies
make update
# or
poetry update

# Export to requirements.txt (for compatibility)
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

## Next Steps

To integrate with a real LLM provider:

1. Update `app/services/chat_service.py` to connect to your LLM API
2. Add API keys to your `.env` file
3. Update `app/core/config.py` to load configuration from environment variables

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
