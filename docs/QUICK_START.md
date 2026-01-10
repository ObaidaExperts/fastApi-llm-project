# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Check

```bash
# Check Python version (should be 3.11.14)
python --version

# Check if Poetry is installed
poetry --version || echo "Poetry not installed - see installation below"
```

## Installation (Choose Your Method)

### Method 1: DevContainer (Easiest - Recommended)

1. Open project in VS Code
2. Click "Reopen in Container" when prompted
3. Wait for container to build (first time takes a few minutes)
4. Everything is automatically set up! ✅

### Method 2: Local Setup with Poetry

```bash
# 1. Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 2. Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# 3. Install dependencies
poetry install

# 4. Set up pre-commit hooks
poetry run pre-commit install

# 5. Verify setup
poetry run pytest  # Should run all tests
```

### Method 3: Using requirements.txt (Legacy)

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run app
uvicorn app.main:app --reload
```

## Verify Installation

```bash
# Run tests (should see 48 passed)
poetry run pytest

# Start the application
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Visit http://localhost:8000/docs
```

## First Commit

```bash
# Review changes
git status

# Add all files
git add .

# Commit
git commit -m "Add production setup: Poetry, Makefile, pre-commit, CI/CD"

# Push
git push
```

## Daily Commands

```bash
# Start development server
poetry run uvicorn app.main:app --reload

# Run tests
poetry run pytest

# Format code
poetry run black app test

# Check code quality
poetry run ruff check app test
```

## That's It! 🎉

You're ready to develop. See `NEXT_STEPS.md` for detailed instructions.
