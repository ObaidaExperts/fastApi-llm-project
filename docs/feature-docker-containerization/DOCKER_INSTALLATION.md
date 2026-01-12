# Docker Installation Guide

## Docker Not Available in Current Environment

Docker is not currently installed in this development environment. This guide provides instructions for installing Docker and testing the containerization setup.

---

## Installation Options

### Option 1: Docker Desktop (Recommended for Windows/Mac)

**Windows (WSL2)**:
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Install Docker Desktop
3. Enable WSL2 integration in Docker Desktop settings
4. Restart your terminal/WSL

**macOS**:
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Install Docker Desktop
3. Start Docker Desktop application

**Linux**:
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
newgrp docker
```

### Option 2: Install Docker in WSL2

```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker service
sudo service docker start

# Verify installation
docker --version
```

---

## Testing Docker Build

Once Docker is installed, you can test the containerization:

### Build the Image

```bash
# Build Docker image
docker build -t fastapi-llm-project:latest .

# Or use Makefile
make docker-build
```

### Run the Container

```bash
# Run container
docker run -p 8000:8000 fastapi-llm-project:latest

# Or use docker-compose
docker-compose up

# Or use Makefile
make docker-up
```

### Test Health Endpoints

```bash
# Health check (liveness)
curl http://localhost:8000/api/v1/health

# Readiness probe
curl http://localhost:8000/api/v1/ready
```

### View Container Logs

```bash
# View logs
docker logs <container-id>

# Or with docker-compose
docker-compose logs -f

# Or use Makefile
make docker-logs
```

---

## Verify Dockerfile Syntax

Even without Docker installed, you can validate the Dockerfile syntax:

### Using hadolint (Dockerfile Linter)

```bash
# Install hadolint (if available)
# Or use online linter: https://hadolint.github.io/hadolint/

# Check Dockerfile
hadolint Dockerfile
```

### Manual Review Checklist

- ✅ Multi-stage build structure
- ✅ Base images specified
- ✅ Environment variables set
- ✅ Dependencies installed
- ✅ Non-root user created
- ✅ Port exposed
- ✅ HEALTHCHECK configured
- ✅ CMD instruction present

---

## Alternative: Test Without Docker

You can still verify the application works locally:

```bash
# Install dependencies
poetry install

# Run application
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test health endpoints
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/ready
```

---

## Dockerfile Validation

The Dockerfile has been validated and includes:

- ✅ Multi-stage build (builder + production)
- ✅ Python 3.11-slim base image
- ✅ Poetry dependency management
- ✅ Non-root user (appuser)
- ✅ Health check configuration
- ✅ Proper port exposure (8000)
- ✅ Security best practices

---

## Next Steps

1. Install Docker using one of the options above
2. Build the Docker image: `docker build -t fastapi-llm-project:latest .`
3. Run the container: `docker run -p 8000:8000 fastapi-llm-project:latest`
4. Test health endpoints
5. Capture screenshots for submission

---

## Troubleshooting

### Docker Command Not Found

- Ensure Docker is installed and running
- Check PATH includes Docker binary
- Restart terminal after installation

### Permission Denied

- Add user to docker group: `sudo usermod -aG docker $USER`
- Log out and log back in
- Or use `sudo docker` (not recommended)

### Build Fails

- Check Dockerfile syntax
- Verify all dependencies are available
- Check disk space
- Review build logs for errors

---

## Resources

- Docker Documentation: https://docs.docker.com/
- Docker Desktop: https://www.docker.com/products/docker-desktop
- Dockerfile Best Practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
