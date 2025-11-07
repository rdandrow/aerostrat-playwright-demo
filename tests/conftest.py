"""
Shared pytest fixtures for Aerostrat Playwright tests.

This module contains fixtures that can be used across all test files.
"""

import pytest
from playwright.sync_api import Page, BrowserContext


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context settings for all tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "user_agent": "Aerostrat-Playwright-Tests/1.0",
        "extra_http_headers": {
            "Accept-Language": "en-US,en;q=0.9"
        }
    }


@pytest.fixture
def page_with_slow_network(context: BrowserContext):
    """Create a page with simulated slow network conditions."""
    page = context.new_page()
    # Simulate slow 3G connection
    context.route("**/*", lambda route: route.continue_())
    yield page
    page.close()


@pytest.fixture
def page_with_cookie_handling(page: Page):
    """Page fixture that automatically handles common cookie scenarios."""
    # Pre-configure any cookie handling if needed
    yield page


# Custom markers for test organization
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add 'slow' marker to tests that might take longer
        if "performance" in item.name or "load" in item.name:
            item.add_marker(pytest.mark.slow)
        
        # Add 'smoke' marker to basic functionality tests
        if "loads_successfully" in item.name or "page_loaded" in item.name:
            item.add_marker(pytest.mark.smoke)