# Aerostrat Playwright Demo

This project contains automated tests for the Aerostrat job posting page using Playwright and the Page Object Model pattern.

## Setup

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install additional testing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install pytest-playwright plugin:**
   ```bash
   playwright install-deps
   ```

## Project Structure

```
aerostrat-playwright-demo/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Shared pytest fixtures
│   ├── page_objects/
│   │   ├── __init__.py
│   │   └── application_overview.py    # Aerostrat job page object model
│   └── test_cases/
│       └── test_aerostrat_job_page.py # Test cases for job page
├── pytest.ini                        # Pytest configuration
├── requirements.txt                   # Python dependencies
└── README.md                         # This file
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run tests with visible browser (headed mode):
```bash
pytest --headed
```

### Run specific test file:
```bash
pytest tests/test_cases/test_aerostrat_job_page.py
```

### Run specific test method:
```bash
pytest tests/test_cases/test_aerostrat_job_page.py::TestAerostratJobPage::test_page_loads_successfully
```

### Run tests with different browsers:
```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

### Run only smoke tests:
```bash
pytest -m smoke
```

### Run tests excluding slow ones:
```bash
pytest -m "not slow"
```

### Generate HTML report:
```bash
pytest --html=report.html --self-contained-html
```

### Run tests in parallel:
```bash
pytest -n auto  # Uses all available CPU cores
pytest -n 4     # Uses 4 parallel processes
```

## Test Categories

- **Smoke Tests**: Basic functionality verification
- **Slow Tests**: Performance and load time tests
- **Visual Tests**: Screenshot comparison tests (currently skipped)

## Page Object Model

The `AerostratJobPage` class in `tests/page_objects/application_overview.py` provides:

- **Navigation**: Navigate to job postings
- **Element Interaction**: Click buttons, scroll to sections
- **Data Extraction**: Get job details, salary info, technical requirements
- **Assertions**: Validate page state and content
- **Error Handling**: Check for error conditions

## Example Test Usage

```python
def test_example(job_page: AerostratJobPage):
    # Navigate and setup
    job_page.navigate_to()
    job_page.wait_for_page_load()
    job_page.dismiss_cookie_notice()
    
    # Validate content
    job_page.assert_job_title("Software Engineer - QA")
    job_page.assert_all_sections_present()
    
    # Extract data
    job_details = job_page.get_job_details()
    salary = job_page.get_salary_range()
    
    # Interact with elements
    job_page.scroll_to_section("benefits")
    job_page.assert_apply_button_visible()
```

## Troubleshooting

1. **Browser not found**: Run `playwright install` to download browsers
2. **Module not found**: Ensure virtual environment is activated
3. **Tests timing out**: Increase timeout values in page object methods
4. **Cookie notice issues**: The tests handle cookie dismissal automatically

## Contributing

1. Add new test methods to `TestAerostratJobPage` class
2. Extend page object model with new locators and methods as needed
3. Use meaningful test names and docstrings
4. Add appropriate pytest markers for test categorization