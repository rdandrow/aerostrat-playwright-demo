"""
Test cases for the Aerostrat job posting page.

This module contains comprehensive tests for the Aerostrat Software Engineer - QA
job posting on Lever, demonstrating the use of the AerostratJobPage page object model.
"""

import pytest
from playwright.sync_api import Page, expect
from tests.page_objects.application_overview import AerostratJobPage


class TestAerostratJobPage:
    """Test class for Aerostrat job page functionality."""
    
    @pytest.fixture
    def job_page(self, page: Page):
        """Fixture to create and return an AerostratJobPage instance."""
        return AerostratJobPage(page)
    
    def test_page_loads_successfully(self, job_page: AerostratJobPage):
        """Test that the job page loads successfully with all required elements."""
        # Navigate to the job page
        job_page.navigate_to()
        
        # Wait for page to load and dismiss cookie notice if present
        job_page.wait_for_page_load()
        job_page.dismiss_cookie_notice()
        
        # Verify page is loaded
        job_page.assert_page_loaded()
        
        # Verify the correct job title
        job_page.assert_job_title("Software Engineer - QA")
    
    def test_job_details_are_displayed(self, job_page: AerostratJobPage):
        """Test that all job details are properly displayed."""
        job_page.navigate_to()
        job_page.wait_for_page_load()
        job_page.dismiss_cookie_notice()
        
        # Get job details
        job_details = job_page.get_job_details()
        
        # Verify job details
        assert job_details["title"] == "Software Engineer - QA"
        assert "Seattle" in job_details["location"]
        assert job_details["remote"] is True
        assert "Software Engineering" in job_details["department"]
        assert "Full-Time" in job_details["type"]
    
    def test_all_job_sections_present(self, job_page: AerostratJobPage):
        """Test that all major job sections are present on the page."""
        job_page.navigate_to()
        job_page.wait_for_page_load()
        job_page.dismiss_cookie_notice()
        
        # Assert all required sections are present
        job_page.assert_all_sections_present()
        
        # Verify individual sections
        sections = job_page.get_job_sections()
        assert sections["about_aerostrat"] is True
        assert sections["responsibilities"] is True
        assert sections["requirements"] is True
        assert sections["compensation"] is True
        assert sections["benefits"] is True
    
    def test_technical_requirements_mentioned(self, job_page: AerostratJobPage):
        """Test that key technical requirements are mentioned in the job posting."""
        job_page.navigate_to()
        job_page.wait_for_page_load()
        job_page.dismiss_cookie_notice()
        
        # Check technical requirements
        tech_requirements = job_page.has_technical_requirements()
        
        # Verify that testing frameworks are mentioned
        assert tech_requirements["playwright"] or tech_requirements["cypress"], \
            "Either Playwright or Cypress should be mentioned"
        
        # Verify Python is mentioned
        assert tech_requirements["python"] is True, "Python should be mentioned in requirements"
        
        # Use the assertion method as well
        job_page.assert_technical_requirements_present()
    
    def test_salary_information_displayed(self, job_page: AerostratJobPage):
        """Test that salary information is clearly displayed."""
        job_page.navigate_to()
        job_page.wait_for_page_load()
        job_page.dismiss_cookie_notice()
        
        # Scroll to compensation section
        job_page.scroll_to_section("compensation")
        
        # Verify salary range is visible
        job_page.assert_salary_range_visible()
        
        # Get and verify salary range
        salary_range = job_page.get_salary_range()
        assert "$100,000" in salary_range
        assert "$150,000" in salary_range
    
    def test_apply_button_functionality(self, job_page: AerostratJobPage):
        """Test that the apply button is visible and functional."""
        job_page.navigate_to()
        job_page.wait_for_page_load()
        job_page.dismiss_cookie_notice()
        
        # Scroll to apply button to ensure it's in view
        job_page.scroll_to_apply_button()
        
        # Verify apply button is visible and enabled
        job_page.assert_apply_button_visible()
        
        # Note: We don't actually click the apply button to avoid submitting applications
        # In a real test environment, you might want to test the application flow
    
    def test_navigation_elements(self, job_page: AerostratJobPage):
        """Test navigation elements like company homepage link."""
        job_page.navigate_to()
        job_page.wait_for_page_load()
        job_page.dismiss_cookie_notice()
        
        # Verify Aerostrat logo/link is present
        expect(job_page.aerostrat_logo).to_be_visible()
        expect(job_page.aerostrat_homepage_link).to_be_visible()
    
    def test_page_content_sections_scroll(self, job_page: AerostratJobPage):
        """Test scrolling to different sections of the job page."""
        job_page.navigate_to()
        job_page.wait_for_page_load()
        job_page.dismiss_cookie_notice()
        
        # Test scrolling to different sections
        sections_to_test = ["about_aerostrat", "responsibilities", "requirements", "compensation", "benefits"]
        
        for section in sections_to_test:
            job_page.scroll_to_section(section)
            # Add a small delay to see the scrolling in action if running with headed browser
            job_page.page.wait_for_timeout(500)
    
    def test_page_title_and_metadata(self, job_page: AerostratJobPage):
        """Test page title and metadata."""
        job_page.navigate_to()
        job_page.wait_for_page_load()
        
        # Get browser page title
        page_title = job_page.get_page_title()
        
        # Verify the page title contains relevant information
        assert "Software Engineer - QA" in page_title
        assert "Aerostrat" in page_title
    
    @pytest.mark.slow
    def test_page_load_performance(self, job_page: AerostratJobPage):
        """Test that the page loads within a reasonable time frame."""
        import time
        
        start_time = time.time()
        job_page.navigate_to()
        job_page.wait_for_page_load(timeout=10000)  # 10 second timeout
        load_time = time.time() - start_time
        
        # Assert page loads within 10 seconds
        assert load_time < 10, f"Page took {load_time:.2f} seconds to load, which is too slow"
        
        # Verify page is properly loaded
        assert job_page.is_page_loaded() is True
    
    def test_error_handling(self, job_page: AerostratJobPage):
        """Test error handling for the page."""
        job_page.navigate_to()
        job_page.wait_for_page_load()
        
        # Verify no error messages are displayed
        job_page.assert_no_errors()
        assert job_page.has_error_message() is False
    
    @pytest.mark.parametrize("job_id,expected_title", [
        ("2cce6cc2-dcdd-4562-af4d-8eb6afd5b281", "Software Engineer - QA"),
        # Add more job IDs here if testing multiple positions
    ])
    def test_different_job_postings(self, job_page: AerostratJobPage, job_id: str, expected_title: str):
        """Test navigation to different job postings by ID."""
        job_page.navigate_to(job_id)
        job_page.wait_for_page_load()
        job_page.dismiss_cookie_notice()
        
        # Verify the correct job title for the specific posting
        actual_title = job_page.get_job_title()
        assert expected_title in actual_title


# Pytest configuration for this test module
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "user_agent": "Mozilla/5.0 (Playwright Test Runner)"
    }


# Example of a test that could be used for visual regression testing
@pytest.mark.skip(reason="Visual testing requires additional setup")
def test_visual_regression(job_page: AerostratJobPage):
    """Example visual regression test (requires screenshot comparison setup)."""
    job_page.navigate_to()
    job_page.wait_for_page_load()
    job_page.dismiss_cookie_notice()
    
    # Take screenshot of the full page
    job_page.page.screenshot(path="tests/screenshots/aerostrat_job_page.png", full_page=True)
    
    # In a real implementation, you would compare this screenshot with a baseline
    # using tools like playwright's built-in visual comparisons or third-party tools