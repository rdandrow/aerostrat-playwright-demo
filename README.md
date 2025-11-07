# Aerostrat Playwright Demo

This project contains comprehensive automated tests for the Aerostrat job posting and application workflow using Playwright and the Page Object Model pattern.

## Current Test Status

**37 Total Tests** - All passing  
**12 Job Overview Tests** - Page content, navigation, performance  
**25 Job Application Tests** - Form automation, validation, file upload  
**Dynamic Data Integration** - Faker library for realistic test scenarios

## Setup

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install additional testing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Key Dependencies:**
   - `playwright` - Browser automation framework
   - `pytest` - Testing framework
   - `pytest-playwright` - Playwright integration for pytest
   - `faker` - Dynamic test data generation
   - `pytest-html` - HTML test reports
   - `pytest-xdist` - Parallel test execution

3. **Install pytest-playwright plugin:**
   ```bash
   playwright install-deps
   ```

## Project Structure

```
aerostrat-playwright-demo/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                          # Shared pytest fixtures
│   ├── page_objects/
│   │   ├── __init__.py
│   │   ├── application_overview.py          # Aerostrat job page object model
│   │   └── application_form.py              # Job application form page object
│   └── test_cases/
│       ├── test_aerostrat_application_overview.py  # Tests for job overview page
│       └── test_aerostrat_job_application.py       # Tests for job application form
├── pytest.ini                              # Pytest configuration
├── requirements.txt                         # Python dependencies
└── README.md                               # This file
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
# Run job overview page tests
pytest tests/test_cases/test_aerostrat_application_overview.py

# Run job application form tests
pytest tests/test_cases/test_aerostrat_job_application.py
```

### Run specific test method:
```bash
# Job overview page test
pytest tests/test_cases/test_aerostrat_application_overview.py::TestAerostratJobPage::test_page_loads_successfully

# Job application form test
pytest tests/test_cases/test_aerostrat_job_application.py::TestAerostratJobApplication::test_application_form_loads_successfully
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

### Job Overview Page
The `AerostratJobPage` class in `tests/page_objects/application_overview.py` provides:

- **Navigation**: Navigate to job postings
- **Element Interaction**: Click buttons, scroll to sections
- **Data Extraction**: Get job details, salary info, technical requirements
- **Assertions**: Validate page state and content
- **Error Handling**: Check for error conditions

### Job Application Form
The `AerostratApplicationFormPage` class in `tests/page_objects/application_form.py` provides:

- **Form Automation**: Fill personal information, upload resume, answer experience questions
- **Dynamic Data Support**: Integration with Faker library for realistic test data
- **Validation Testing**: Form validation and error handling
- **Complete Workflows**: End-to-end application form completion
- **Experience Levels**: Handle different experience level selections for technical questions

## Example Test Usage

### Job Overview Page Tests
```python
def test_job_page_example(job_page: AerostratJobPage):
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

### Job Application Form Tests
```python
def test_application_form_example(application_form: AerostratApplicationFormPage, fake, sample_resume_file):
    # Navigate and setup
    application_form.navigate_to()
    application_form.wait_for_page_load()
    application_form.dismiss_cookie_notice()
    
    # Fill form with dynamic data
    application_form.fill_personal_information(
        full_name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        location=f"{fake.city()}, {fake.state_abbr()}",
        company=fake.company(),
        pronouns=Pronouns.THEY_THEM
    )
    
    # Upload resume and answer questions
    application_form.upload_resume(sample_resume_file)
    application_form.answer_experience_questions(
        e2e_automation=ExperienceLevel.TWO_TO_FOUR,
        python=ExperienceLevel.FIVE_PLUS,
        playwright=ExperienceLevel.ONE_TO_TWO,
        automation_types=ExperienceLevel.TWO_TO_FOUR
    )
    
    # Validate form completion
    application_form.assert_submit_button_enabled()
```

## Troubleshooting

1. **Browser not found**: Run `playwright install` to download browsers
2. **Module not found**: Ensure virtual environment is activated
3. **Tests timing out**: Increase timeout values in page object methods
4. **Cookie notice issues**: The tests handle cookie dismissal automatically

## Test Features

### Dynamic Test Data
- **Faker Integration**: All tests use the Faker library for realistic, varied test data
- **Randomized Scenarios**: Each test run uses different data to catch edge cases
- **Realistic Data**: Names, emails, phone numbers, locations, and companies that mirror real user input

### Comprehensive Coverage
- **Job Overview Tests**: 12 tests covering page loading, content validation, and navigation
- **Application Form Tests**: 25 tests covering form filling, validation, file upload, and workflows
- **Experience Levels**: Parametrized tests for all experience level combinations
- **Error Handling**: Robust validation and error state testing

### Browser Compatibility
- **Multi-browser Support**: Tests run on Chromium, Firefox, and WebKit
- **Responsive Design**: Tests work across different viewport sizes
- **Cross-platform**: Compatible with macOS, Windows, and Linux

## Contributing

1. Add new test methods to `TestAerostratJobPage` or `TestAerostratJobApplication` classes
2. Extend page object models with new locators and methods as needed
3. Use Faker for dynamic test data instead of hardcoded values
4. Use meaningful test names and docstrings
5. Add appropriate pytest markers for test categorization
6. Follow the Page Object Model pattern for maintainable tests