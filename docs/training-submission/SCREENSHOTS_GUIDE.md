# Screenshots Guide for Training Submission

This guide will help you capture the necessary screenshots for your team lead submission.

## Required Screenshots

### 1. API Documentation (Swagger UI)
**Purpose**: Show the implemented endpoints with authentication

**Steps**:
1. Start the server: `make run` or `poetry run uvicorn app.main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. Take screenshot showing:
   - The Swagger UI interface
   - `/api/v1/auth/login` endpoint
   - `/api/v1/auth/callback` endpoint
   - `/api/v1/auth/me` endpoint
   - `/api/v1/chat/stream` endpoint with lock icon (requires auth)
   - The "Authorize" button at the top

**File name**: `screenshot-01-swagger-ui.png`

---

### 2. API Key Authentication Success
**Purpose**: Demonstrate API key authentication working

**Steps**:
1. Use Postman, Thunder Client (VS Code), or curl
2. Make a POST request to: `http://localhost:8000/api/v1/chat/stream`
3. Add header: `X-API-Key: test-api-key-123`
4. Add body:
   ```json
   {
     "messages": [{"role": "user", "content": "Hello"}]
   }
   ```
5. Take screenshot showing:
   - Request headers (highlighting X-API-Key)
   - Request body
   - Successful 200 response
   - Response headers showing `X-Auth-Method: api_key` and `X-User-ID`

**File name**: `screenshot-02-api-key-success.png`

---

### 3. OAuth Authentication Flow
**Purpose**: Show OAuth login and token generation

**Steps**:
1. Open browser or use curl
2. Navigate to: `http://localhost:8000/api/v1/auth/login`
3. Should redirect to callback with demo code
4. Take screenshot of callback response showing:
   - `access_token`
   - `token_type: bearer`
   - `expires_in`

**Alternative**: Show the full flow:
- Screenshot 3a: Login endpoint redirect
- Screenshot 3b: Callback response with token

**File name**: `screenshot-03-oauth-token.png`

---

### 4. OAuth Bearer Token Usage
**Purpose**: Demonstrate using OAuth token for authentication

**Steps**:
1. Get token from step 3 (e.g., `oauth_demo_auth_code_12345`)
2. Make POST request to: `http://localhost:8000/api/v1/chat/stream`
3. Add header: `Authorization: Bearer oauth_demo_auth_code_12345`
4. Take screenshot showing:
   - Request with Authorization header
   - Successful 200 response
   - Response headers showing `X-Auth-Method: oauth`

**File name**: `screenshot-04-oauth-bearer-success.png`

---

### 5. Rate Limit Headers
**Purpose**: Show rate limiting headers in responses

**Steps**:
1. Make any authenticated request (API key or OAuth)
2. Check response headers
3. Take screenshot showing:
   - `X-RateLimit-Limit-Minute: 60`
   - `X-RateLimit-Limit-Hour: 1000`
   - `X-RateLimit-Remaining-Minute: 59`
   - `X-RateLimit-Remaining-Hour: 999`

**File name**: `screenshot-05-rate-limit-headers.png`

---

### 6. Rate Limit Exceeded (429 Error)
**Purpose**: Demonstrate rate limiting protection

**Steps**:
1. Use a script or tool to make rapid requests
2. Example script:
   ```bash
   for i in {1..65}; do
     curl -X POST http://localhost:8000/api/v1/chat/stream \
       -H "X-API-Key: test-api-key-123" \
       -H "Content-Type: application/json" \
       -d '{"messages":[{"role":"user","content":"test"}]}'
     echo "Request $i"
   done
   ```
3. Take screenshot showing:
   - Multiple successful requests (200)
   - Then HTTP 429 response
   - Error message: "Rate limit exceeded: 60 requests per minute"
   - Rate limit headers in error response

**File name**: `screenshot-06-rate-limit-exceeded.png`

---

### 7. Authentication Failure (401 Error)
**Purpose**: Show proper error handling for missing/invalid auth

**Steps**:
1. Make request WITHOUT authentication header
2. Or use invalid API key: `X-API-Key: invalid-key`
3. Take screenshot showing:
   - Request without auth headers
   - HTTP 401 Unauthorized response
   - Error message: "Authentication required..."
   - `WWW-Authenticate` header

**File name**: `screenshot-07-auth-failure.png`

---

### 8. Test Results & Coverage
**Purpose**: Demonstrate comprehensive testing

**Steps**:
1. Run tests: `poetry run pytest --cov=app --cov-report=html -v`
2. Take screenshot showing:
   - Test execution results (48 passed)
   - Coverage summary (93% coverage)
   - Or open `htmlcov/index.html` and screenshot coverage report

**File name**: `screenshot-08-test-results.png`

---

### 9. Project Structure
**Purpose**: Show code organization

**Steps**:
1. Open VS Code file explorer
2. Expand key directories:
   - `app/core/` (auth, config files)
   - `app/middleware/` (rate limit, auth middleware)
   - `app/api/v1/` (endpoints)
   - `test/` (test files)
3. Take screenshot showing the organized structure

**File name**: `screenshot-09-project-structure.png`

---

### 10. Code Example (Authentication)
**Purpose**: Show implementation code

**Steps**:
1. Open `app/core/auth.py` in VS Code
2. Highlight the `get_auth_context()` function
3. Take screenshot showing:
   - Clean, well-documented code
   - Type hints
   - Error handling

**File name**: `screenshot-10-auth-code.png`

---

### 11. Code Example (Rate Limiting)
**Purpose**: Show rate limiting implementation

**Steps**:
1. Open `app/middleware/rate_limit.py`
2. Highlight the `RateLimitMiddleware` class
3. Take screenshot showing:
   - Middleware implementation
   - Rate limit checking logic
   - Header setting

**File name**: `screenshot-11-rate-limit-code.png`

---

## Quick Screenshot Checklist

- [ ] Swagger UI with endpoints
- [ ] API Key authentication success
- [ ] OAuth token generation
- [ ] OAuth Bearer token usage
- [ ] Rate limit headers in response
- [ ] Rate limit exceeded (429)
- [ ] Authentication failure (401)
- [ ] Test results with coverage
- [ ] Project structure
- [ ] Authentication code example
- [ ] Rate limiting code example

## Tips for Better Screenshots

1. **Use a clean browser/IDE**: Close unnecessary tabs
2. **Highlight important parts**: Use annotations or arrows
3. **Include context**: Show URL bar, status codes, headers
4. **Consistent naming**: Use the suggested file names
5. **Good resolution**: Ensure text is readable
6. **Multiple angles**: Show both request and response when relevant

## Tools for Screenshots

- **Windows**: Snipping Tool, Windows + Shift + S
- **Mac**: Cmd + Shift + 4
- **Linux**: Flameshot, Spectacle, or built-in screenshot tools
- **VS Code**: Use built-in screenshot extensions or external tools

---

## Creating a Screenshot Summary Document

After capturing screenshots, create a document that:
1. Lists each screenshot with a brief description
2. Explains what each screenshot demonstrates
3. References the screenshot files

Example:
```markdown
# Screenshot Summary

1. **API Documentation** (screenshot-01-swagger-ui.png)
   - Shows all implemented endpoints in Swagger UI
   - Demonstrates authentication requirements with lock icons

2. **API Key Authentication** (screenshot-02-api-key-success.png)
   - Successful request using X-API-Key header
   - Response shows X-Auth-Method: api_key header
   ...
```
