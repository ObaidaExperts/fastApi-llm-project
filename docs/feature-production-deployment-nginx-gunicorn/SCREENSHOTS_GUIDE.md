# Screenshots Guide: Production Deployment with Gunicorn & Nginx

This guide will help you capture the necessary screenshots for your team lead submission.

## Required Screenshots

### 1. Gunicorn Configuration File
**Purpose**: Show Gunicorn production configuration

**Steps**:
1. Open `gunicorn.conf.py` in VS Code
2. Highlight key configuration sections (workers, bind, timeouts)
3. Take screenshot showing:
   - Worker configuration
   - Performance settings
   - Security settings
   - Logging configuration

**File name**: `screenshot-01-gunicorn-config.png`

---

### 2. Nginx Configuration File
**Purpose**: Show Nginx reverse proxy configuration

**Steps**:
1. Open `nginx.conf` or `deployment/nginx-site.conf` in VS Code
2. Highlight upstream and location blocks
3. Take screenshot showing:
   - Upstream backend configuration
   - Rate limiting zones
   - Location blocks
   - Security headers

**File name**: `screenshot-02-nginx-config.png`

---

### 3. Systemd Service File
**Purpose**: Show systemd service configuration

**Steps**:
1. Open `deployment/gunicorn.service` in VS Code
2. Highlight security settings and service configuration
3. Take screenshot showing:
   - Service definition
   - Security hardening options
   - Process management settings

**File name**: `screenshot-03-systemd-service.png`

---

### 4. Deployment Script
**Purpose**: Show automated deployment script

**Steps**:
1. Open `deployment/deploy.sh` in VS Code
2. Highlight key sections
3. Take screenshot showing:
   - Script structure
   - Service setup
   - Error handling

**File name**: `screenshot-04-deployment-script.png`

---

### 5. Gunicorn Running (if possible)
**Purpose**: Show Gunicorn process running

**Steps**:
1. If you have access to a server, run: `ps aux | grep gunicorn`
2. Or show systemd status: `sudo systemctl status fastapi-llm`
3. Take screenshot showing:
   - Gunicorn processes
   - Worker processes
   - Process details

**File name**: `screenshot-05-gunicorn-processes.png`

---

### 6. Nginx Configuration Test
**Purpose**: Show Nginx configuration validation

**Steps**:
1. Run: `sudo nginx -t`
2. Take screenshot showing:
   - Configuration test command
   - Success message
   - Configuration file paths

**File name**: `screenshot-06-nginx-test.png`

---

### 7. Service Status Check
**Purpose**: Show systemd service status

**Steps**:
1. Run: `sudo systemctl status fastapi-llm`
2. Take screenshot showing:
   - Service status (active/running)
   - Service information
   - Recent log entries

**File name**: `screenshot-07-service-status.png`

---

### 8. Nginx Status Check
**Purpose**: Show Nginx service status

**Steps**:
1. Run: `sudo systemctl status nginx`
2. Take screenshot showing:
   - Nginx status
   - Active connections
   - Service information

**File name**: `screenshot-08-nginx-status.png`

---

### 9. Configuration File Structure
**Purpose**: Show deployment file organization

**Steps**:
1. Open VS Code file explorer
2. Expand `deployment/` directory
3. Take screenshot showing:
   - All deployment files
   - Configuration files
   - File structure

**File name**: `screenshot-09-file-structure.png`

---

### 10. Gunicorn Logs
**Purpose**: Show Gunicorn logging output

**Steps**:
1. Run: `sudo journalctl -u fastapi-llm -n 50`
2. Take screenshot showing:
   - Log entries
   - Worker startup messages
   - Request logs

**File name**: `screenshot-10-gunicorn-logs.png`

---

### 11. Nginx Access Logs
**Purpose**: Show Nginx access logs

**Steps**:
1. Run: `sudo tail -f /var/log/nginx/fastapi_access.log`
2. Make a test request
3. Take screenshot showing:
   - Access log entries
   - Request details
   - Response codes

**File name**: `screenshot-11-nginx-access-logs.png`

---

### 12. Performance Test (if possible)
**Purpose**: Show application running behind Nginx

**Steps**:
1. Make request to application through Nginx
2. Use curl or browser: `curl http://localhost/api/v1/health`
3. Take screenshot showing:
   - Request/response
   - Headers
   - Response time

**File name**: `screenshot-12-performance-test.png`

---

### 13. Rate Limiting Test
**Purpose**: Show rate limiting in action

**Steps**:
1. Make rapid requests: `for i in {1..15}; do curl http://localhost/api/v1/health; done`
2. Take screenshot showing:
   - Successful requests
   - Rate limit response (429)
   - Rate limit headers

**File name**: `screenshot-13-rate-limiting.png`

---

## Quick Screenshot Checklist

- [ ] Gunicorn configuration file
- [ ] Nginx configuration file
- [ ] Systemd service file
- [ ] Deployment script
- [ ] Gunicorn processes (if available)
- [ ] Nginx configuration test
- [ ] Service status check
- [ ] Nginx status check
- [ ] Configuration file structure
- [ ] Gunicorn logs
- [ ] Nginx access logs
- [ ] Performance test
- [ ] Rate limiting test

## Tips for Better Screenshots

1. **Show full context**: Include command prompts and outputs
2. **Highlight important parts**: Use annotations or arrows
3. **Good resolution**: Ensure all text is readable
4. **Consistent naming**: Use suggested file names
5. **Multiple views**: Show both configuration and runtime when relevant

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

1. **Gunicorn Configuration** (screenshot-01-gunicorn-config.png)
   - Shows production Gunicorn settings
   - Worker configuration
   - Performance optimizations

2. **Nginx Configuration** (screenshot-02-nginx-config.png)
   - Shows reverse proxy setup
   - Rate limiting configuration
   - Security headers
   ...
```
