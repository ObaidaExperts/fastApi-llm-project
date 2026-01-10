# Test Suite

This directory contains unit tests for the FastAPI LLM Chat Service.

## Test Structure

```
test/
├── __init__.py
├── conftest.py              # Pytest fixtures and configuration
├── test_api_key_auth.py     # API key authentication tests
├── test_oauth.py            # OAuth authentication tests
├── test_auth.py             # Unified authentication tests
├── test_rate_limit.py       # Rate limiting middleware tests
├── test_auth_middleware.py  # Authentication middleware tests
├── test_endpoints.py        # API endpoint tests
└── test_config.py           # Configuration tests
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage report
```bash
pytest --cov=app --cov-report=html
```

### Run specific test file
```bash
pytest test/test_api_key_auth.py
```

### Run specific test
```bash
pytest test/test_api_key_auth.py::TestAPIKeyAuth::test_verify_api_key_value_valid
```

### Run with verbose output
```bash
pytest -v
```

### Run tests in parallel (if pytest-xdist is installed)
```bash
pytest -n auto
```

## Test Coverage

The test suite covers:

- **API Key Authentication**: Valid/invalid keys, missing keys, multiple keys
- **OAuth Authentication**: Bearer tokens, token validation, error handling
- **Unified Authentication**: API key precedence, OAuth fallback, no auth scenarios
- **Rate Limiting**: Per-minute/hour limits, user-based limiting, IP fallback
- **Middleware**: Auth extraction, rate limit enforcement, endpoint bypassing
- **Endpoints**: Chat endpoint, auth endpoints, health endpoint
- **Configuration**: Settings validation, default values

## Fixtures

Common fixtures are defined in `conftest.py`:

- `client`: FastAPI TestClient instance
- `mock_api_key`: Valid test API key
- `mock_oauth_token`: Valid test OAuth token
- `mock_chat_request`: Mock chat request payload
- `mock_settings`: Mocked settings for testing

## Writing New Tests

When adding new tests:

1. Create a new file `test_<module_name>.py`
2. Import necessary modules and fixtures
3. Use descriptive test class names: `Test<FeatureName>`
4. Use descriptive test method names: `test_<what_is_being_tested>`
5. Use fixtures from `conftest.py` when possible
6. Mark async tests with `@pytest.mark.asyncio`

Example:
```python
import pytest
from app.core.some_module import some_function

class TestSomeFeature:
    def test_some_function_valid_input(self):
        result = some_function("valid")
        assert result == expected_value
    
    @pytest.mark.asyncio
    async def test_some_async_function(self):
        result = await some_async_function("input")
        assert result is not None
```

## Continuous Integration

Tests should pass before merging code. The test suite is designed to:

- Run quickly (< 30 seconds)
- Be deterministic (no flaky tests)
- Cover critical paths
- Be maintainable and readable
