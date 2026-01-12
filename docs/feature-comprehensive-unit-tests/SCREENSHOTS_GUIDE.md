# Screenshots Guide: Comprehensive Unit Tests

This guide will help you capture the necessary screenshots for your team lead submission.

## Required Screenshots

### 1. Test Execution Results
**Purpose**: Show all tests passing

**Steps**:
1. Run: `poetry run pytest -v`
2. Take screenshot showing:
   - All 107 tests passing
   - Test execution summary
   - No failures or errors

**File name**: `screenshot-01-all-tests-passing.png`

---

### 2. Test Coverage Report
**Purpose**: Show test coverage statistics

**Steps**:
1. Run: `poetry run pytest --cov=app --cov-report=term-missing`
2. Take screenshot showing:
   - Coverage percentage (95%+)
   - Coverage breakdown by module
   - Missing lines (if any)

**File name**: `screenshot-02-coverage-report.png`

---

### 3. HTML Coverage Report
**Purpose**: Show detailed coverage visualization

**Steps**:
1. Run: `poetry run pytest --cov=app --cov-report=html`
2. Open `htmlcov/index.html` in browser
3. Take screenshot showing:
   - Coverage overview
   - Module list with coverage percentages
   - Color-coded coverage indicators

**File name**: `screenshot-03-html-coverage.png`

---

### 4. Model Tests Execution
**Purpose**: Show Pydantic model tests

**Steps**:
1. Run: `poetry run pytest test/test_models.py -v`
2. Take screenshot showing:
   - All model test classes
   - Test results (31 tests)
   - All passing

**File name**: `screenshot-04-model-tests.png`

---

### 5. Streaming Tests Execution
**Purpose**: Show streaming behavior tests

**Steps**:
1. Run: `poetry run pytest test/test_streaming.py -v`
2. Take screenshot showing:
   - Streaming service tests
   - Streaming endpoint tests
   - All 11 tests passing

**File name**: `screenshot-05-streaming-tests.png`

---

### 6. Edge Case Tests Execution
**Purpose**: Show edge case and error handling tests

**Steps**:
1. Run: `poetry run pytest test/test_endpoint_edge_cases.py -v`
2. Take screenshot showing:
   - Edge case test classes
   - All 17 tests passing
   - Error scenario coverage

**File name**: `screenshot-06-edge-case-tests.png`

---

### 7. Model Test Example - Validation Error
**Purpose**: Show model validation testing

**Steps**:
1. Open `test/test_models.py` in VS Code
2. Find a test that checks validation errors (e.g., `test_chat_message_invalid_role`)
3. Run that specific test: `poetry run pytest test/test_models.py::TestChatMessage::test_chat_message_invalid_role -v`
4. Take screenshot showing:
   - Test code
   - Test execution
   - ValidationError being raised correctly

**File name**: `screenshot-07-model-validation-test.png`

---

### 8. Streaming Test Example
**Purpose**: Show streaming test implementation

**Steps**:
1. Open `test/test_streaming.py` in VS Code
2. Highlight a streaming test (e.g., `test_stream_chat_tokens_structure`)
3. Take screenshot showing:
   - Test code with async/await
   - Test logic
   - Assertions

**File name**: `screenshot-08-streaming-test-code.png`

---

### 9. Edge Case Test Example
**Purpose**: Show edge case test implementation

**Steps**:
1. Open `test/test_endpoint_edge_cases.py` in VS Code
2. Highlight an edge case test (e.g., `test_chat_endpoint_empty_messages_array`)
3. Take screenshot showing:
   - Test code
   - Error scenario testing
   - Assertions for error responses

**File name**: `screenshot-09-edge-case-test-code.png`

---

### 10. Test Organization Structure
**Purpose**: Show test file organization

**Steps**:
1. Open VS Code file explorer
2. Expand `test/` directory
3. Take screenshot showing:
   - All test files
   - New test files highlighted:
     - test_models.py
     - test_streaming.py
     - test_endpoint_edge_cases.py
   - File structure

**File name**: `screenshot-10-test-structure.png`

---

### 11. Pytest Output with Verbose Mode
**Purpose**: Show detailed test execution

**Steps**:
1. Run: `poetry run pytest -v --tb=short`
2. Take screenshot showing:
   - Detailed test names
   - Test execution flow
   - Pass/fail indicators
   - Execution time

**File name**: `screenshot-11-verbose-test-output.png`

---

### 12. Coverage by Module
**Purpose**: Show coverage breakdown

**Steps**:
1. Run: `poetry run pytest --cov=app --cov-report=term`
2. Scroll to show specific modules
3. Take screenshot showing:
   - Models: 100% coverage
   - Services: 100% coverage
   - Endpoints coverage
   - Overall statistics

**File name**: `screenshot-12-coverage-breakdown.png`

---

## Quick Screenshot Checklist

- [ ] All tests passing (107 tests)
- [ ] Coverage report (95%+)
- [ ] HTML coverage visualization
- [ ] Model tests execution
- [ ] Streaming tests execution
- [ ] Edge case tests execution
- [ ] Model validation test example
- [ ] Streaming test code example
- [ ] Edge case test code example
- [ ] Test file structure
- [ ] Verbose test output
- [ ] Coverage breakdown by module

## Tips for Better Screenshots

1. **Use terminal with good contrast**: Ensure text is readable
2. **Show full context**: Include command prompts and outputs
3. **Highlight important parts**: Use annotations if needed
4. **Consistent naming**: Use suggested file names
5. **Good resolution**: Ensure all text is clear
6. **Multiple views**: Show both code and execution when relevant

## Tools for Screenshots

- **Windows**: Snipping Tool, Windows + Shift + S
- **Mac**: Cmd + Shift + 4
- **Linux**: Flameshot, Spectacle, or built-in tools
- **VS Code**: Use built-in screenshot extensions or external tools

---

## Creating a Screenshot Summary

After capturing screenshots, create a document that:
1. Lists each screenshot with description
2. Explains what each demonstrates
3. References the screenshot files

Example:
```markdown
# Screenshot Summary

1. **All Tests Passing** (screenshot-01-all-tests-passing.png)
   - Shows 107 tests passing
   - Demonstrates comprehensive test coverage
   - No failures or errors

2. **Coverage Report** (screenshot-02-coverage-report.png)
   - Shows 95%+ coverage
   - Breakdown by module
   - Missing lines highlighted
   ...
```
