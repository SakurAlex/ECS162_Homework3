# Backend Testing Instructions

## Prerequisites
- Python 3.x
- Virtual environment (venv)

## Setup (If not already done)
1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests
If you have already set up the virtual environment and installed dependencies, simply run:
```bash
python -m pytest --cov=app --cov-report=term-missing -v
```

This command will:
- Run all tests in the `tests` directory
- Generate coverage report for the `app` module
- Show missing lines in the coverage report
- Display verbose output

## Test Results
The test results will show:
- Number of passed/failed tests
- Code coverage percentage
- Missing lines in the coverage report
- Detailed test output for each test case 