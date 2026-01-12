# Screenshots Guide: Pydantic Models & OpenAPI Documentation

This guide will help you capture the necessary screenshots for your team lead submission.

## Required Screenshots

### 1. Swagger UI - Main Page with All Endpoints
**Purpose**: Show the complete API documentation with all endpoints

**Steps**:
1. Start the server: `make run` or `poetry run uvicorn app.main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. Take screenshot showing:
   - All endpoints listed (health, auth, chat)
   - Tags visible (health, authentication, chat)
   - "Authorize" button at top
   - API title and description

**File name**: `screenshot-01-swagger-main.png`

---

### 2. Swagger UI - Health Endpoint Schema
**Purpose**: Show HealthResponse model in OpenAPI

**Steps**:
1. In Swagger UI, expand `GET /api/v1/health`
2. Click "Try it out" → "Execute"
3. Scroll to "Response" section
4. Take screenshot showing:
   - Request endpoint details
   - Response schema showing `HealthResponse` model
   - Example response with `status` and `trace_id`
   - Model properties visible

**File name**: `screenshot-02-health-schema.png`

---

### 3. Swagger UI - Chat Request Model
**Purpose**: Show ChatRequest model with examples

**Steps**:
1. In Swagger UI, expand `POST /api/v1/chat/stream`
2. Scroll to "Request body" section
3. Take screenshot showing:
   - `ChatRequest` model schema
   - `messages` array with `ChatMessage` items
   - Example request body
   - Field descriptions visible
   - "Try it out" button

**File name**: `screenshot-03-chat-request-model.png`

---

### 4. Swagger UI - ChatMessage Model Details
**Purpose**: Show detailed ChatMessage model schema

**Steps**:
1. In Swagger UI, click on "Schemas" section (bottom of page)
2. Find and expand `ChatMessage`
3. Take screenshot showing:
   - Model properties (role, content)
   - Field descriptions
   - Examples
   - Validation rules (enum for role, minLength for content)

**File name**: `screenshot-04-chat-message-schema.png`

---

### 5. Swagger UI - OAuth Token Response Model
**Purpose**: Show OAuthTokenResponse model

**Steps**:
1. In Swagger UI, expand `GET /api/v1/auth/callback`
2. Scroll to "Responses" section
3. Expand "200" response
4. Take screenshot showing:
   - `OAuthTokenResponse` schema
   - Properties: access_token, token_type, expires_in
   - Example response
   - Field descriptions

**File name**: `screenshot-05-oauth-token-schema.png`

---

### 6. Swagger UI - UserInfoResponse Model
**Purpose**: Show UserInfoResponse model

**Steps**:
1. In Swagger UI, expand `GET /api/v1/auth/me`
2. Scroll to "Responses" section
3. Expand "200" response
4. Take screenshot showing:
   - `UserInfoResponse` schema
   - Properties: user_id, auth_method
   - Example response
   - Pattern validation for auth_method visible

**File name**: `screenshot-06-user-info-schema.png`

---

### 7. Swagger UI - All Schemas Section
**Purpose**: Show all available models in OpenAPI schema

**Steps**:
1. In Swagger UI, scroll to bottom
2. Click "Schemas" section
3. Take screenshot showing:
   - List of all models:
     - ChatMessage
     - ChatRequest
     - HealthResponse
     - OAuthTokenResponse
     - UserInfoResponse
   - All models expandable

**File name**: `screenshot-07-all-schemas.png`

---

### 8. Swagger UI - Request Validation Example
**Purpose**: Show model validation in action

**Steps**:
1. In Swagger UI, expand `POST /api/v1/chat/stream`
2. Click "Try it out"
3. Modify the example request to have invalid data:
   - Empty messages array: `{"messages": []}`
   - Or empty content: `{"messages": [{"role": "user", "content": ""}]}`
4. Click "Execute"
5. Take screenshot showing:
   - Validation error response
   - Error message showing validation failure
   - Field-level error details

**File name**: `screenshot-08-validation-error.png`

---

### 9. ReDoc Documentation
**Purpose**: Show alternative documentation format

**Steps**:
1. Open browser: `http://localhost:8000/redoc`
2. Take screenshot showing:
   - ReDoc interface
   - All endpoints listed
   - Model schemas visible
   - Clean, readable format

**File name**: `screenshot-09-redoc.png`

---

### 10. OpenAPI JSON Schema
**Purpose**: Show raw OpenAPI schema generation

**Steps**:
1. Open browser: `http://localhost:8000/openapi.json`
2. Search for "ChatRequest" or scroll to "components" → "schemas"
3. Take screenshot showing:
   - OpenAPI JSON structure
   - ChatRequest schema definition
   - All properties and validation rules
   - Examples included

**File name**: `screenshot-10-openapi-json.png`

---

### 11. Code Example - Model Definition
**Purpose**: Show Pydantic model code

**Steps**:
1. Open `app/models/chat.py` in VS Code
2. Highlight `ChatRequest` or `ChatMessage` class
3. Take screenshot showing:
   - Model class definition
   - Field definitions with descriptions
   - Examples in model_config
   - Type hints

**File name**: `screenshot-11-model-code.png`

---

### 12. Code Example - Endpoint Using Model
**Purpose**: Show endpoint using response_model

**Steps**:
1. Open `app/api/v1/health.py` in VS Code
2. Highlight the endpoint function with `response_model=HealthResponse`
3. Take screenshot showing:
   - Endpoint definition
   - `response_model` parameter
   - Return type hint
   - Model import

**File name**: `screenshot-12-endpoint-code.png`

---

### 13. Successful API Request with Validation
**Purpose**: Show model validation working correctly

**Steps**:
1. Use Postman/Thunder Client or curl
2. Make POST request to `/api/v1/chat/stream` with valid `ChatRequest`
3. Take screenshot showing:
   - Request body (valid ChatRequest)
   - Successful 200 response
   - Response headers
   - Streaming response data

**File name**: `screenshot-13-valid-request.png`

---

## Quick Screenshot Checklist

- [ ] Swagger UI main page
- [ ] Health endpoint schema
- [ ] Chat request model
- [ ] ChatMessage model details
- [ ] OAuth token response model
- [ ] UserInfo response model
- [ ] All schemas section
- [ ] Validation error example
- [ ] ReDoc documentation
- [ ] OpenAPI JSON schema
- [ ] Model code example
- [ ] Endpoint code example
- [ ] Successful validated request

## Tips for Better Screenshots

1. **Use browser zoom**: Set to 80-90% to capture more content
2. **Highlight important parts**: Use annotations or arrows
3. **Show context**: Include URL bar, status codes, response times
4. **Consistent naming**: Use suggested file names
5. **Good resolution**: Ensure text is readable
6. **Multiple views**: Show both request and response when relevant

## Tools for Screenshots

- **Windows**: Snipping Tool, Windows + Shift + S
- **Mac**: Cmd + Shift + 4
- **Linux**: Flameshot, Spectacle, or built-in tools
- **VS Code**: Use built-in screenshot extensions or external tools

---

## Creating a Screenshot Summary

After capturing screenshots, create a document that:
1. Lists each screenshot with description
2. Explains what each demonstrates
3. References the screenshot files

Example:
```markdown
# Screenshot Summary

1. **Swagger UI Main Page** (screenshot-01-swagger-main.png)
   - Shows complete API documentation
   - All endpoints visible with proper tags
   - Demonstrates automatic OpenAPI generation

2. **Health Endpoint Schema** (screenshot-02-health-schema.png)
   - Shows HealthResponse model in action
   - Example response with proper structure
   ...
```
