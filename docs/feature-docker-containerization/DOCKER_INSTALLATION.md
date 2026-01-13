# Docker Installation Guide

## Docker in Dev Container Environment

**Note**: You are currently working in a VS Code Dev Container. Docker is not installed inside the dev container by default. This guide provides options for testing Docker builds in this environment.

---

## Options for Dev Container Users

### Option 1: Use Docker from Host Machine (Recommended)

Since you're in a dev container, you can use Docker from your host machine:

**Windows/Mac with Docker Desktop**:
1. Ensure Docker Desktop is running on your host machine
2. Build and test Docker images from your host terminal (outside the dev container)
3. Or configure dev container to mount Docker socket (see Option 3)

**From Host Terminal**:
```bash
# Navigate to project directory on host
cd /path/to/fastApi-llm-project

# Build Docker image
docker build -t fastapi-llm-project:latest .

# Run container
docker run -p 8000:8000 fastapi-llm-project:latest
```

### Option 2: Configure Dev Container with Docker-in-Docker

Add Docker support to your dev container by updating `.devcontainer/devcontainer.json`:

```json
{
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  "mounts": [
    "source=/var/run/docker.sock,target=/var/run/docker-host.sock,type=bind"
  ]
}
```

Then rebuild your dev container. Docker will be available inside the container.

### Option 3: Install Docker in Dev Container (Not Recommended)

You can install Docker inside the dev container, but this is not recommended as it requires privileged mode.

---

## Installation Options (For Host Machine)

### Option A: Docker Desktop (Recommended for Windows/Mac)

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

## Alternative: Test Without Docker (In Dev Container)

You can verify the application and health endpoints work without Docker:

```bash
# Dependencies are already installed in dev container
# Just run the application
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Test health endpoints (in another terminal or from host)
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/ready
```

**Note**: The dev container is configured to auto-start the application on port 8000, so you may already have it running!

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
