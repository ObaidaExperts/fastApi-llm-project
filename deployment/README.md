# Production Deployment Guide

This directory contains production deployment configurations for FastAPI application with Gunicorn and Nginx.

## Files

- `gunicorn.service` - Systemd service file for Gunicorn
- `nginx-site.conf` - Nginx site configuration
- `deploy.sh` - Automated deployment script

## Quick Start

1. Copy files to server
2. Run deployment script: `sudo ./deploy.sh`
3. Configure domain name in nginx-site.conf
4. Start services: `sudo systemctl start fastapi-llm && sudo systemctl restart nginx`

## Manual Setup

### 1. Install Gunicorn

```bash
poetry add gunicorn
```

### 2. Setup Gunicorn Service

```bash
sudo cp deployment/gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fastapi-llm
sudo systemctl start fastapi-llm
```

### 3. Setup Nginx

```bash
sudo cp deployment/nginx-site.conf /etc/nginx/sites-available/fastapi-llm-project
sudo ln -s /etc/nginx/sites-available/fastapi-llm-project /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Configuration

Edit `gunicorn.conf.py` for Gunicorn settings.
Edit `nginx-site.conf` for Nginx settings.

## Monitoring

```bash
# Check Gunicorn status
sudo systemctl status fastapi-llm

# Check Nginx status
sudo systemctl status nginx

# View logs
sudo journalctl -u fastapi-llm -f
sudo tail -f /var/log/nginx/fastapi_error.log
```
