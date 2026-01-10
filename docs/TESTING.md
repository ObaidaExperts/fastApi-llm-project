# Testing Authentication and Rate Limiting

This document provides examples for testing the implemented authentication and rate limiting features.

## Prerequisites

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the FastAPI server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Testing API Key Authentication

### Test 1: Valid API Key
```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "X-API-Key: test-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

Expected: Success with response headers including `X-Auth-Method: api_key` and `X-User-ID: user1`

### Test 2: Invalid API Key
```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "X-API-Key: invalid-key" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

Expected: 401 Unauthorized with error message

### Test 3: Missing API Key
```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

Expected: 401 Unauthorized with error message

## Testing OAuth Authentication

### Test 1: Valid OAuth Token
```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Authorization: Bearer oauth_test123" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

Expected: Success with response headers including `X-Auth-Method: oauth` and `X-User-ID: user_test123`

### Test 2: Invalid OAuth Token
```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Authorization: Bearer invalid_token" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

Expected: 401 Unauthorized with error message

## Testing Rate Limiting

### Test 1: Rate Limit Per Minute
Send 65 requests quickly (exceeding the 60/minute limit):

```bash
for i in {1..65}; do
  echo "Request $i"
  curl -X POST "http://localhost:8000/api/v1/chat/stream" \
    -H "X-API-Key: test-api-key-123" \
    -H "Content-Type: application/json" \
    -d '{"messages": [{"role": "user", "content": "Hello"}]}' \
    -w "\nStatus: %{http_code}\n"
done
```

Expected: First 60 requests succeed, request 61+ returns 429 Too Many Requests

### Test 2: Rate Limit Headers
```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "X-API-Key: test-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}' \
  -v
```

Expected: Response headers include:
- `X-RateLimit-Limit-Minute: 60`
- `X-RateLimit-Limit-Hour: 1000`
- `X-RateLimit-Remaining-Minute: <number>`
- `X-RateLimit-Remaining-Hour: <number>`

## Testing OAuth Endpoints

### Test OAuth Login Flow
```bash
curl "http://localhost:8000/api/v1/auth/login"
```

Expected: Redirect response to OAuth provider

### Test OAuth Callback
```bash
curl "http://localhost:8000/api/v1/auth/callback?code=test123"
```

Expected: JSON response with access_token

### Test Get Current User (requires valid token)
```bash
curl -H "Authorization: Bearer oauth_test123" \
  "http://localhost:8000/api/v1/auth/me"
```

Expected: JSON response with user_id and auth_method

## Testing Health Endpoint (No Auth Required)

```bash
curl "http://localhost:8000/api/v1/health"
```

Expected: Success without authentication requirement

## Using Python Requests

```python
import requests

# API Key Authentication
response = requests.post(
    "http://localhost:8000/api/v1/chat/stream",
    headers={"X-API-Key": "test-api-key-123"},
    json={"messages": [{"role": "user", "content": "Hello"}]}
)
print(response.status_code)
print(response.headers)

# OAuth Authentication
response = requests.post(
    "http://localhost:8000/api/v1/chat/stream",
    headers={"Authorization": "Bearer oauth_test123"},
    json={"messages": [{"role": "user", "content": "Hello"}]}
)
print(response.status_code)
print(response.headers)
```

## Viewing API Documentation

Visit http://localhost:8000/docs to see the interactive API documentation with authentication options.
