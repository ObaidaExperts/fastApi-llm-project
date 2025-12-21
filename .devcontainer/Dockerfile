FROM python:3.11-slim

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (recommended by VS Code)
RUN useradd -ms /bin/bash vscode
USER vscode

WORKDIR /workspace

# Upgrade pip
RUN pip install --upgrade pip
