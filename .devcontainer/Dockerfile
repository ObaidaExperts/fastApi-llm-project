FROM python:3.11-slim

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip && \
    pip install poetry==1.7.1 && \
    poetry config virtualenvs.create false

# Create non-root user (recommended by VS Code)
RUN useradd -ms /bin/bash vscode
USER vscode

WORKDIR /workspace

# Set Poetry to not create virtualenvs (we're in a container)
ENV POETRY_VENV_IN_PROJECT=false
ENV POETRY_NO_INTERACTION=1
