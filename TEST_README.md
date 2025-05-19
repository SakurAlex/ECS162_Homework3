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

# Frontend Testing Instructions

## Prerequisites
- Node.js (latest LTS version)
- npm (comes with Node.js)

## Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running Tests
There are several ways to run the tests:

1. Run tests once:
```bash
npm test
```

2. Run tests in watch mode (recommended during development):
```bash
npm run test:watch
```

3. Run tests with coverage report:
```bash
npm run coverage
```

## Test Structure
- Tests are located in `src/__tests__` directory
- Each component has its corresponding test file (e.g., `Comments.spec.ts` for `Comments.svelte`)
- Tests use Vitest as the test runner and @testing-library/svelte for component testing

## Writing Tests
Example test structure:
```typescript
import { describe, it, expect } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/svelte'
import YourComponent from '../YourComponent.svelte'

describe('YourComponent.svelte', () => {
  it('should render correctly', () => {
    render(YourComponent, { props: { /* your props */ } })
    expect(screen.getByText('Some Text')).toBeInTheDocument()
  })
})
```

## Test Environment
- Tests run in a JSDOM environment
- Global browser APIs are mocked (localStorage, fetch, etc.)
- Each test is isolated with automatic cleanup
- Browser testing is enabled with Chrome in headless mode

## Common Testing Utilities
- `render`: Mount Svelte components
- `screen`: Query DOM elements
- `fireEvent`: Simulate user interactions
- `expect`: Make assertions
- `vi.fn()`: Create mock functions 