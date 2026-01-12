# Training Project Deliverables: Production Deployment with Gunicorn & Nginx

## Project Description

Implementation of production-ready deployment configuration using Gunicorn as ASGI server and Nginx as reverse proxy, with performance and security optimizations.

### What are Gunicorn and Nginx?

**Gunicorn** (Green Unicorn) is a Python WSGI/ASGI HTTP Server for UNIX that runs Python web applications. It manages multiple worker processes to handle concurrent requests, provides process management, and integrates seamlessly with FastAPI through Uvicorn workers. Gunicorn is production-ready, handling worker lifecycle, graceful restarts, and process monitoring [1].

**Nginx** is a high-performance web server and reverse proxy that acts as a front-end server handling client requests and forwarding them to backend application servers like Gunicorn. It provides SSL termination, load balancing, rate limiting, static file serving, and caching. In this setup, Nginx receives all client requests, applies security policies and rate limiting, then proxies requests to Gunicorn workers, significantly improving performance and security [2].

**References:**
- [1] Gunicorn Documentation: https://docs.gunicorn.org/
- [2] Nginx Documentation: https://nginx.org/en/docs/

---

## 1. What Was Done

### 1.1 Gunicorn Configuration (`gunicorn.conf.py`)

Created production-ready Gunicorn configuration:

**Server Configuration**:
- Bind address: Configurable via `GUNICORN_BIND` (default: 127.0.0.1:8000)
- Backlog: 2048 connections
- Worker class: `uvicorn.workers.UvicornWorker` for ASGI support

**Worker Configuration**:
- Workers: Auto-calculated (CPU cores * 2 + 1) or configurable
- Worker connections: 1000 per worker
- Timeout: 120 seconds
- Keepalive: 5 seconds

**Performance Optimizations**:
- Preload app: Enabled for faster startup
- Max requests: 1000 per worker (with jitter for graceful restarts)
- Connection pooling: Optimized for high concurrency

**Security Settings**:
- Request limits: Line (4094), fields (100), field size (8190)
- Graceful timeout: 30 seconds
- Process isolation: User/group configuration

**Logging**:
- Access logs: Configurable (default: stdout)
- Error logs: Configurable (default: stderr)
- Log level: Configurable (default: info)
- Custom access log format with timing

### 1.2 Nginx Reverse Proxy Configuration (`nginx.conf`)

Created production-ready Nginx configuration:

**Upstream Configuration**:
- Backend servers: Load balanced with `least_conn` algorithm
- Health checks: Max fails and timeout configuration
- Keepalive connections: 32 connections

**Rate Limiting**:
- API endpoints: 10 requests/second with burst of 20
- Auth endpoints: 5 requests/second with burst of 10
- Separate zones for different endpoint types

**Security Headers**:
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin
- Server tokens: Hidden

**Performance Optimizations**:
- Gzip compression: Enabled with optimal settings
- Client buffering: Optimized buffer sizes
- Timeouts: Configured for long-running requests (streaming)
- Proxy buffering: Disabled for streaming endpoints

**Location Blocks**:
- `/health`: Health check endpoint (no rate limiting)
- `/api/`: API endpoints with rate limiting
- `/api/v1/auth/`: Auth endpoints with stricter rate limiting
- `/docs`, `/redoc`, `/openapi.json`: Documentation (restrictable)

**SSL/HTTPS Support**:
- HTTPS server block template included
- Modern TLS configuration (TLSv1.2, TLSv1.3)
- HSTS header configuration

### 1.3 Systemd Service (`deployment/gunicorn.service`)

Created systemd service file for Gunicorn:

**Service Configuration**:
- Type: notify (for proper startup coordination)
- User/Group: www-data (configurable)
- Working directory: Application directory
- Environment: PATH and PYTHONPATH configured

**Security Hardening**:
- NoNewPrivileges: true
- ProtectSystem: strict
- ProtectHome: true
- PrivateTmp: yes
- PrivateDevices: yes
- MemoryDenyWriteExecute: yes
- SystemCallFilter: Restricted to @system-service
- RestrictAddressFamilies: Limited to necessary families

**Process Management**:
- Auto-restart: Always with 10-second delay
- Graceful shutdown: 5-second timeout
- Reload support: HUP signal handling

### 1.4 Deployment Script (`deployment/deploy.sh`)

Created automated deployment script:

**Features**:
- System dependency installation
- Python virtual environment setup
- Poetry dependency installation
- Service configuration
- Nginx configuration
- Log directory setup
- Service startup and status checking

**Safety**:
- Root check
- Error handling (set -e)
- Status verification
- Color-coded output

### 1.5 Production Environment Template (`.env.production.example`)

Created production environment variables template:
- API configuration
- OAuth settings
- Rate limiting configuration
- Gunicorn settings
- Security flags

---

## 2. Performance Optimizations

### 2.1 Gunicorn Optimizations

- **Worker Calculation**: Automatic based on CPU cores
- **Preload App**: Faster worker startup
- **Connection Pooling**: Efficient connection reuse
- **Graceful Restarts**: Max requests with jitter
- **Keepalive**: Reduced connection overhead

### 2.2 Nginx Optimizations

- **Gzip Compression**: Reduced bandwidth usage
- **Connection Keepalive**: Reduced connection overhead
- **Load Balancing**: Least connection algorithm
- **Buffering**: Optimized for streaming
- **Caching Headers**: Configurable caching

### 2.3 Security Optimizations

- **Rate Limiting**: Per-endpoint rate limits
- **Security Headers**: Multiple security headers
- **Request Limits**: Size and field limits
- **Process Isolation**: Systemd security features
- **SSL/TLS**: Modern TLS configuration

---

## 3. Configuration Files

### 3.1 Gunicorn (`gunicorn.conf.py`)
- Production-ready configuration
- Environment variable support
- Performance tuning
- Security settings
- Logging configuration

### 3.2 Nginx (`nginx.conf` and `deployment/nginx-site.conf`)
- Reverse proxy configuration
- Rate limiting
- Security headers
- Performance optimizations
- SSL/HTTPS support

### 3.3 Systemd (`deployment/gunicorn.service`)
- Service definition
- Security hardening
- Auto-restart configuration
- Process management

### 3.4 Deployment (`deployment/deploy.sh`)
- Automated setup script
- Dependency installation
- Service configuration
- Status verification

---

## 4. Deployment Steps

### 4.1 Prerequisites
- Ubuntu/Debian server
- Root/sudo access
- Domain name (optional)

### 4.2 Installation Steps

1. **Copy application files** to `/opt/fastapi-llm-project`
2. **Run deployment script**: `sudo ./deployment/deploy.sh`
3. **Configure domain** in nginx-site.conf
4. **Set environment variables** in `.env.production`
5. **Start services**: `sudo systemctl start fastapi-llm && sudo systemctl restart nginx`

### 4.3 Manual Configuration

```bash
# Install dependencies
poetry add gunicorn

# Setup Gunicorn service
sudo cp deployment/gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fastapi-llm

# Setup Nginx
sudo cp deployment/nginx-site.conf /etc/nginx/sites-available/fastapi-llm-project
sudo ln -s /etc/nginx/sites-available/fastapi-llm-project /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 5. Monitoring & Maintenance

### 5.1 Service Management

```bash
# Check status
sudo systemctl status fastapi-llm
sudo systemctl status nginx

# View logs
sudo journalctl -u fastapi-llm -f
sudo tail -f /var/log/nginx/fastapi_error.log

# Restart services
sudo systemctl restart fastapi-llm
sudo systemctl restart nginx
```

### 5.2 Performance Monitoring

- Gunicorn worker status
- Nginx connection counts
- Response times
- Error rates
- Rate limit hits

---

## 6. Security Features

### 6.1 Gunicorn Security
- Request size limits
- Process isolation
- User/group restrictions
- System call filtering

### 6.2 Nginx Security
- Rate limiting
- Security headers
- Request validation
- SSL/TLS support
- Access restrictions

### 6.3 Systemd Security
- No new privileges
- Protected system paths
- Private tmp/devices
- Memory protection
- Restricted system calls

---

## 7. Files Created/Modified

### Created Files
- `gunicorn.conf.py` - Gunicorn configuration
- `nginx.conf` - Nginx configuration template
- `deployment/gunicorn.service` - Systemd service file
- `deployment/nginx-site.conf` - Nginx site configuration
- `deployment/deploy.sh` - Deployment script
- `deployment/README.md` - Deployment guide
- `.env.production.example` - Production environment template

### Modified Files
- `pyproject.toml` - Added gunicorn dependency

---

## 8. Benefits Achieved

### 8.1 Performance
- High concurrency support
- Efficient resource usage
- Optimized for streaming
- Reduced latency

### 8.2 Security
- Rate limiting protection
- Security headers
- Process isolation
- Request validation

### 8.3 Reliability
- Auto-restart on failure
- Graceful shutdowns
- Health checks
- Load balancing

### 8.4 Maintainability
- Automated deployment
- Clear configuration
- Comprehensive logging
- Easy monitoring

---

## Conclusion

This implementation provides a production-ready deployment setup with Gunicorn and Nginx, optimized for performance, security, and reliability. The configuration supports high concurrency, includes comprehensive security measures, and provides easy deployment and monitoring capabilities.
