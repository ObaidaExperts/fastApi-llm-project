.PHONY: help install install-dev run test lint format format-check type-check precommit clean docker-build docker-run

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	poetry install --no-dev

install-dev: ## Install all dependencies including dev dependencies
	poetry install

run: ## Run the FastAPI application
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-prod: ## Run the FastAPI application in production mode
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000

test: ## Run tests with pytest
	poetry run pytest

test-cov: ## Run tests with coverage report
	poetry run pytest --cov=app --cov-report=html --cov-report=term-missing

test-watch: ## Run tests in watch mode
	poetry run pytest-watch

lint: ## Run linting checks (ruff)
	poetry run ruff check app test

lint-fix: ## Fix linting issues automatically
	poetry run ruff check --fix app test

format: ## Format code with black and isort
	poetry run black app test
	poetry run isort app test

format-check: ## Check code formatting without making changes
	poetry run black --check app test
	poetry run isort --check-only app test

type-check: ## Run type checking with mypy
	poetry run mypy app

precommit: format-check lint type-check test ## Run all pre-commit checks

validate-openapi: ## Validate OpenAPI schema generation
	poetry run python scripts/validate_openapi.py

ci-check: ## Run all CI checks locally (format, lint, type-check, test, validate-openapi)
	@echo "Running all CI checks locally..."
	@make format-check
	@make lint
	@make type-check
	@make test-cov
	@make validate-openapi
	@echo "✅ All CI checks passed!"

clean: ## Clean cache files and build artifacts
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	rm -rf dist build .ruff_cache

docker-build: ## Build Docker image
	docker build -t fastapi-llm-project:latest .

docker-run: ## Run Docker container
	docker run -p 8000:8000 --env-file .env fastapi-llm-project:latest

shell: ## Open a shell with poetry environment activated
	poetry shell

update: ## Update dependencies
	poetry update
