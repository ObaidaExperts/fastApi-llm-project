# Screenshots Guide: CI/CD Code Quality & Testing

This guide will help you capture the necessary screenshots for your team lead submission.

## Required Screenshots

### 1. GitHub Actions Workflow File
**Purpose**: Show CI workflow configuration

**Steps**:
1. Open `.github/workflows/ci.yml` in VS Code
2. Highlight the workflow structure
3. Take screenshot showing:
   - Workflow triggers (on push/PR)
   - Job definitions
   - Steps in each job

**File name**: `screenshot-01-ci-workflow.png`

---

### 2. GitHub Actions - Workflow Run (Success)
**Purpose**: Show successful CI execution

**Steps**:
1. Push code to GitHub (or view existing runs)
2. Go to GitHub repository → Actions tab
3. Click on latest workflow run
4. Take screenshot showing:
   - All jobs passing (green checkmarks)
   - Job execution times
   - Summary of checks

**File name**: `screenshot-02-ci-success.png`

---

### 3. Code Quality Job Details
**Purpose**: Show code quality checks execution

**Steps**:
1. In GitHub Actions, expand "Code Quality Checks" job
2. Expand each step (Black, isort, Ruff, mypy)
3. Take screenshot showing:
   - All checks passing
   - Check outputs
   - Execution times

**File name**: `screenshot-03-code-quality-job.png`

---

### 4. Unit Tests Job Details
**Purpose**: Show test execution and coverage

**Steps**:
1. In GitHub Actions, expand "Unit Tests" job
2. Expand test execution step
3. Take screenshot showing:
   - Test results (X passed)
   - Coverage percentage
   - Coverage threshold check

**File name**: `screenshot-04-unit-tests-job.png`

---

### 5. OpenAPI Validation Job Details
**Purpose**: Show OpenAPI validation execution

**Steps**:
1. In GitHub Actions, expand "OpenAPI Documentation Validation" job
2. Expand validation step
3. Take screenshot showing:
   - Validation script output
   - Success message
   - Schema statistics

**File name**: `screenshot-05-openapi-validation-job.png`

---

### 6. Coverage Report Artifact
**Purpose**: Show coverage HTML report

**Steps**:
1. In GitHub Actions run, scroll to "Artifacts" section
2. Download "coverage-report" artifact
3. Open `htmlcov/index.html` in browser
4. Take screenshot showing:
   - Coverage overview
   - Module coverage percentages
   - Overall coverage

**File name**: `screenshot-06-coverage-report.png`

---

### 7. OpenAPI Schema Artifact
**Purpose**: Show generated OpenAPI schema

**Steps**:
1. In GitHub Actions run, download "openapi-schema" artifact
2. Open `openapi_schema.json` in editor
3. Take screenshot showing:
   - Schema structure
   - Paths section
   - Components/schemas section

**File name**: `screenshot-07-openapi-schema.png`

---

### 8. Local CI Check Execution
**Purpose**: Show running CI checks locally

**Steps**:
1. Run: `make ci-check`
2. Take screenshot showing:
   - Command execution
   - All checks running
   - Success messages

**File name**: `screenshot-08-local-ci-check.png`

---

### 9. OpenAPI Validation Script
**Purpose**: Show validation script code

**Steps**:
1. Open `scripts/validate_openapi.py` in VS Code
2. Highlight key validation functions
3. Take screenshot showing:
   - Script structure
   - Validation logic
   - Error handling

**File name**: `screenshot-09-validation-script.png`

---

### 10. CI Workflow Run on Failed Check
**Purpose**: Show CI catching an error

**Steps**:
1. Intentionally introduce a formatting error
2. Push to GitHub
3. View failed workflow run
4. Take screenshot showing:
   - Failed job (red X)
   - Error message
   - Which check failed

**File name**: `screenshot-10-ci-failure.png`

---

### 11. Ruff Linting Output
**Purpose**: Show Ruff linting results

**Steps**:
1. In GitHub Actions, expand Ruff step
2. Or run locally: `poetry run ruff check app test`
3. Take screenshot showing:
   - Linting output
   - Issues found (if any)
   - Check completion

**File name**: `screenshot-11-ruff-output.png`

---

### 12. mypy Type Checking Output
**Purpose**: Show mypy type checking results

**Steps**:
1. In GitHub Actions, expand mypy step
2. Or run locally: `poetry run mypy app`
3. Take screenshot showing:
   - Type checking output
   - Errors/warnings (if any)
   - Check completion

**File name**: `screenshot-12-mypy-output.png`

---

### 13. Test Execution Output
**Purpose**: Show pytest execution

**Steps**:
1. In GitHub Actions, expand test execution step
2. Or run locally: `poetry run pytest -v`
3. Take screenshot showing:
   - Test execution
   - Test results
   - Coverage summary

**File name**: `screenshot-13-test-output.png`

---

## Quick Screenshot Checklist

- [ ] CI workflow file
- [ ] Successful CI run
- [ ] Code quality job details
- [ ] Unit tests job details
- [ ] OpenAPI validation job details
- [ ] Coverage report artifact
- [ ] OpenAPI schema artifact
- [ ] Local CI check execution
- [ ] Validation script code
- [ ] CI failure example
- [ ] Ruff linting output
- [ ] mypy type checking output
- [ ] Test execution output

## Tips for Better Screenshots

1. **Show full context**: Include GitHub UI, terminal prompts
2. **Highlight important parts**: Use annotations if needed
3. **Good resolution**: Ensure all text is readable
4. **Consistent naming**: Use suggested file names
5. **Multiple views**: Show both code and execution

## Tools for Screenshots

- **Windows**: Snipping Tool, Windows + Shift + S
- **Mac**: Cmd + Shift + 4
- **Linux**: Flameshot, Spectacle, or built-in tools
- **VS Code**: Use built-in screenshot extensions

---

## Creating a Screenshot Summary

After capturing screenshots, create a document that:
1. Lists each screenshot with description
2. Explains what each demonstrates
3. References the screenshot files

Example:
```markdown
# Screenshot Summary

1. **CI Workflow File** (screenshot-01-ci-workflow.png)
   - Shows GitHub Actions workflow configuration
   - Three main jobs defined
   - Triggers on push and PR

2. **Successful CI Run** (screenshot-02-ci-success.png)
   - Shows all jobs passing
   - Green checkmarks for all checks
   ...
```
