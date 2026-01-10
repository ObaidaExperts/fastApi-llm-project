# Next Steps - Production Setup

Follow these steps to complete the production setup and start developing.

## Step 1: Install Poetry

Poetry is required for dependency management. Install it using one of these methods:

### Option A: Official Installer (Recommended)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Option B: pip (if you prefer)
```bash
pip install poetry
```

### Option C: Using DevContainer (Easiest)
The DevContainer already has Poetry installed. Just reopen the project in VS Code and select "Reopen in Container".

### Verify Installation
```bash
poetry --version
```

### Add Poetry to PATH (if needed)
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

## Step 2: Install Dependencies

Once Poetry is installed:

```bash
# Install all dependencies (including dev dependencies)
poetry install

# Or if Make is available:
make install-dev
```

This will:
- Create a virtual environment (if not using DevContainer)
- Install all production dependencies
- Install all development dependencies (pytest, black, ruff, etc.)

## Step 3: Set Up Pre-commit Hooks

Pre-commit hooks will automatically check code quality before each commit:

```bash
poetry run pre-commit install
```

This installs the hooks. They will run automatically on `git commit`.

### Test Pre-commit Hooks Manually
```bash
poetry run pre-commit run --all-files
```

## Step 4: Verify Everything Works

### Test the Application
```bash
# Using Poetry
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or if Make is available:
make run
```

Visit http://localhost:8000/docs to see the API documentation.

### Run Tests
```bash
# Using Poetry
poetry run pytest

# Or if Make is available:
make test
```

All 48 tests should pass ✅

### Run Code Quality Checks
```bash
# Format code
poetry run black app test
poetry run isort app test

# Lint code
poetry run ruff check app test

# Type check
poetry run mypy app

# Or run all checks at once (if Make is available):
make precommit
```

## Step 5: Commit Your Changes

Once everything is verified, commit the production setup:

```bash
# Review changes
git status

# Add all new files
git add .

# Commit
git commit -m "Add production setup: Poetry, Makefile, pre-commit hooks, CI/CD

- Add pyproject.toml with Poetry dependency management
- Add Makefile with developer convenience commands
- Add pre-commit hooks for code quality
- Add GitHub Actions CI workflow
- Update DevContainer with Poetry support
- Update README with new setup instructions
- Add .python-version for pyenv
- Add comprehensive .gitignore"

# Push to remote
git push
```

## Step 6: Verify CI/CD

After pushing:

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. You should see the CI workflow running
4. It should pass all checks ✅

## Step 7: Start Developing

Now you're ready to develop! Here's your daily workflow:

### Daily Development Workflow

1. **Start the application:**
   ```bash
   make run
   # or
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Make your changes** in the code

3. **Before committing, run checks:**
   ```bash
   make precommit
   # or manually:
   poetry run black app test
   poetry run ruff check app test
   poetry run pytest
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Your commit message"
   # Pre-commit hooks will run automatically
   ```

5. **Push to remote:**
   ```bash
   git push
   # CI will run automatically
   ```

## Troubleshooting

### Poetry Command Not Found
```bash
# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or reinstall Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

### Make Command Not Found
- **Windows:** Install via Chocolatey (`choco install make`) or use WSL
- **macOS:** Install Xcode Command Line Tools (`xcode-select --install`)
- **Linux:** `sudo apt-get install build-essential` (Ubuntu/Debian)

**Note:** Make is optional. You can use Poetry commands directly instead.

### Virtual Environment Issues
```bash
# Remove existing venv
rm -rf .venv

# Reinstall with Poetry
poetry install
```

### Pre-commit Hooks Not Running
```bash
# Reinstall hooks
poetry run pre-commit install --overwrite
```

### Tests Failing
```bash
# Run with verbose output
poetry run pytest -v

# Run specific test file
poetry run pytest test/test_auth.py -v
```

## Quick Reference

### Common Commands

| Task | Command |
|------|---------|
| Install dependencies | `poetry install` or `make install-dev` |
| Run app | `poetry run uvicorn app.main:app --reload` or `make run` |
| Run tests | `poetry run pytest` or `make test` |
| Format code | `poetry run black app test` or `make format` |
| Lint code | `poetry run ruff check app test` or `make lint` |
| Run all checks | `make precommit` |
| Clean caches | `make clean` |

### Using Poetry Shell

Instead of prefixing every command with `poetry run`, you can activate the Poetry shell:

```bash
poetry shell
# Now you're in the virtual environment
pytest
uvicorn app.main:app --reload
# etc.
```

## What's Next?

1. ✅ **Complete Step 1-4** above to set up your environment
2. ✅ **Commit the production setup** (Step 5)
3. ✅ **Verify CI/CD works** (Step 6)
4. 🚀 **Start developing** using the daily workflow (Step 7)

## Need Help?

- Check `PRODUCTION_SETUP.md` for detailed explanations
- Check `README.md` for project overview
- Check `docs/` folder for implementation details
- Check `test/README.md` for testing information

Happy coding! 🎉
