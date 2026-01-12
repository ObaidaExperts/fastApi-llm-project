# Screenshots Guide: Docker Containerization

This guide will help you capture the necessary screenshots for your team lead submission.

## Required Screenshots

### 1. Dockerfile Content
**Purpose**: Show Dockerfile implementation

**Steps**:
1. Open `Dockerfile` in VS Code
2. Highlight the multi-stage build structure
3. Take screenshot showing:
   - Builder stage
   - Production stage
   - Health check configuration
   - Non-root user setup

**File name**: `screenshot-01-dockerfile.png`

---

### 2. Docker Build Process
**Purpose**: Show successful Docker image build

**Steps**:
1. Run: `docker build -t fastapi-llm-project:latest .`
2. Take screenshot showing:
   - Build process output
   - Success message
   - Image size information

**File name**: `screenshot-02-docker-build.png`

---

### 3. Docker Image List
**Purpose**: Show created Docker image

**Steps**:
1. Run: `docker images fastapi-llm-project`
2. Take screenshot showing:
   - Image name and tag
   - Image size
   - Creation date

**File name**: `screenshot-03-docker-images.png`

---

### 4. Container Running
**Purpose**: Show container running successfully

**Steps**:
1. Run: `docker run -d -p 8000:8000 --name fastapi-test fastapi-llm-project:latest`
2. Run: `docker ps`
3. Take screenshot showing:
   - Container status (Up)
   - Port mapping
   - Container name

**File name**: `screenshot-04-container-running.png`

---

### 5. Health Check Endpoint
**Purpose**: Show health check endpoint response

**Steps**:
1. Ensure container is running
2. Run: `curl http://localhost:8000/api/v1/health`
3. Or open in browser: `http://localhost:8000/api/v1/health`
4. Take screenshot showing:
   - HTTP response (200 OK)
   - JSON response with status and trace_id

**File name**: `screenshot-05-health-check.png`

---

### 6. Readiness Probe Endpoint
**Purpose**: Show readiness probe endpoint response

**Steps**:
1. Ensure container is running
2. Run: `curl http://localhost:8000/api/v1/ready`
3. Or open in browser: `http://localhost:8000/api/v1/ready`
4. Take screenshot showing:
   - HTTP response (200 OK)
   - JSON response with status, trace_id, and checks

**File name**: `screenshot-06-readiness-probe.png`

---

### 7. Docker Compose Up
**Purpose**: Show docker-compose startup

**Steps**:
1. Run: `docker-compose up -d`
2. Take screenshot showing:
   - Service creation
   - Container startup
   - Success messages

**File name**: `screenshot-07-docker-compose-up.png`

---

### 8. Docker Compose Logs
**Purpose**: Show application logs

**Steps**:
1. Run: `docker-compose logs fastapi-app`
2. Or: `docker logs fastapi-test`
3. Take screenshot showing:
   - Application startup logs
   - Uvicorn server running
   - Port binding information

**File name**: `screenshot-08-docker-logs.png`

---

### 9. Docker Health Check Status
**Purpose**: Show Docker health check status

**Steps**:
1. Run: `docker inspect --format='{{json .State.Health}}' fastapi-test | jq`
2. Or: `docker ps` (shows health status)
3. Take screenshot showing:
   - Health status (healthy)
   - Health check history
   - Last check time

**File name**: `screenshot-09-health-status.png`

---

### 10. API Documentation in Container
**Purpose**: Show API docs accessible in container

**Steps**:
1. Open browser: `http://localhost:8000/docs`
2. Navigate to health endpoints
3. Take screenshot showing:
   - Swagger UI
   - Health endpoints visible
   - Endpoint documentation

**File name**: `screenshot-10-api-docs.png`

---

### 11. Container Stats
**Purpose**: Show container resource usage

**Steps**:
1. Run: `docker stats fastapi-test`
2. Wait a few seconds for stats to populate
3. Take screenshot showing:
   - CPU usage
   - Memory usage
   - Network I/O

**File name**: `screenshot-11-container-stats.png`

---

### 12. .dockerignore File
**Purpose**: Show .dockerignore configuration

**Steps**:
1. Open `.dockerignore` in VS Code
2. Highlight key exclusions
3. Take screenshot showing:
   - File structure
   - Exclusion patterns
   - Comments explaining exclusions

**File name**: `screenshot-12-dockerignore.png`

---

### 13. Readiness Probe Code
**Purpose**: Show readiness probe implementation

**Steps**:
1. Open `app/api/v1/health.py` in VS Code
2. Highlight readiness probe endpoint
3. Take screenshot showing:
   - `/ready` endpoint definition
   - Database check logic
   - Response structure

**File name**: `screenshot-13-readiness-code.png`

---

## Quick Screenshot Checklist

- [ ] Dockerfile content
- [ ] Docker build process
- [ ] Docker image list
- [ ] Container running
- [ ] Health check endpoint
- [ ] Readiness probe endpoint
- [ ] Docker Compose up
- [ ] Docker logs
- [ ] Docker health check status
- [ ] API documentation in container
- [ ] Container stats
- [ ] .dockerignore file
- [ ] Readiness probe code

## Tips for Better Screenshots

1. **Show full context**: Include terminal prompts, browser address bar
2. **Highlight important parts**: Use annotations if needed
3. **Good resolution**: Ensure all text is readable
4. **Consistent naming**: Use suggested file names
5. **Multiple views**: Show both code and execution

## Tools for Screenshots

- **Windows**: Snipping Tool, Windows + Shift + S
- **Mac**: Cmd + Shift + 4
- **Linux**: Flameshot, Spectacle, or built-in tools
- **VS Code**: Use built-in screenshot extensions

---

## Creating a Screenshot Summary

After capturing screenshots, create a document that:
1. Lists each screenshot with description
2. Explains what each demonstrates
3. References the screenshot files

Example:
```markdown
# Screenshot Summary

1. **Dockerfile Content** (screenshot-01-dockerfile.png)
   - Shows multi-stage build structure
   - Health check configuration
   - Non-root user setup

2. **Docker Build Process** (screenshot-02-docker-build.png)
   - Shows successful image build
   - Build output and image size
   ...
```
