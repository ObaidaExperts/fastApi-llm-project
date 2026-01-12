#!/bin/bash
# Production deployment script for FastAPI application with Gunicorn and Nginx

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/opt/fastapi-llm-project"
SERVICE_USER="www-data"
SERVICE_GROUP="www-data"
VENV_DIR="${APP_DIR}/.venv"

echo -e "${GREEN}Starting deployment...${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

# Create application directory
echo -e "${YELLOW}Creating application directory...${NC}"
mkdir -p "${APP_DIR}"
chown -R ${SERVICE_USER}:${SERVICE_GROUP} "${APP_DIR}"

# Install system dependencies
echo -e "${YELLOW}Installing system dependencies...${NC}"
apt-get update
apt-get install -y python3 python3-pip python3-venv nginx gunicorn

# Setup Python virtual environment
echo -e "${YELLOW}Setting up Python virtual environment...${NC}"
if [ ! -d "${VENV_DIR}" ]; then
    python3 -m venv "${VENV_DIR}"
fi

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
"${VENV_DIR}/bin/pip" install --upgrade pip
"${VENV_DIR}/bin/pip" install poetry
cd "${APP_DIR}"
"${VENV_DIR}/bin/poetry" install --no-dev

# Copy application files (assuming code is already in APP_DIR)
echo -e "${YELLOW}Setting up application files...${NC}"
chown -R ${SERVICE_USER}:${SERVICE_GROUP} "${APP_DIR}"
chmod +x "${APP_DIR}/gunicorn.conf.py"

# Setup Gunicorn systemd service
echo -e "${YELLOW}Setting up Gunicorn systemd service...${NC}"
cp "${APP_DIR}/deployment/gunicorn.service" /etc/systemd/system/fastapi-llm.service
systemctl daemon-reload
systemctl enable fastapi-llm.service

# Setup Nginx configuration
echo -e "${YELLOW}Setting up Nginx configuration...${NC}"
cp "${APP_DIR}/deployment/nginx-site.conf" /etc/nginx/sites-available/fastapi-llm-project
ln -sf /etc/nginx/sites-available/fastapi-llm-project /etc/nginx/sites-enabled/
nginx -t

# Create log directories
echo -e "${YELLOW}Creating log directories...${NC}"
mkdir -p /var/log/nginx
touch /var/log/nginx/fastapi_access.log
touch /var/log/nginx/fastapi_error.log
chown ${SERVICE_USER}:${SERVICE_GROUP} /var/log/nginx/fastapi_*.log

# Start services
echo -e "${YELLOW}Starting services...${NC}"
systemctl start fastapi-llm.service
systemctl restart nginx

# Check service status
echo -e "${YELLOW}Checking service status...${NC}"
systemctl status fastapi-llm.service --no-pager
systemctl status nginx --no-pager

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}Application should be accessible at http://your-domain.com${NC}"
