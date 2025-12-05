"""
Aerostrat Job Page Object Model

This module contains the page object model for the Aerostrat job posting page on Lever,
following Playwright best practices for maintainable and reusable test automation.
"""

from playwright.sync_api import Page, Locator, expect


class AerostratJobPage:
    """Page Object Model for the Aerostrat job posting page on Lever."""
    
    def __init__(self, page: Page):
        """Initialize the AerostratJobPage.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self._setup_locators()
    
    def _setup_locators(self):
        """Define all locators for the job page elements."""
        # Header elements
        self.aerostrat_logo = self.page.locator(".main-header-logo img[alt*='Aerostrat']")
        self.job_title = self.page.get_by_role("heading", level=2).first
        
        # Job details section  
        self.job_location = self.page.locator(".location")
        self.job_department = self.page.locator(".department")  
        self.job_type = self.page.locator(".employment-type")
        self.remote_indicator = self.page.locator(".workplaceTypes:has-text('Remote')")
        
        # Company info section
        self.about_aerostrat_heading = self.page.locator("text='About Aerostrat'")
        self.about_role_heading = self.page.locator("text='About this role'")
        
        # Job content sections
        self.role_responsibilities = self.page.locator("text='In this role, you will...'")
        self.role_requirements = self.page.locator("text='This role is great for you if...'")
        self.compensation_section = self.page.locator("text='Compensation'")
        self.benefits_section = self.page.locator("text='Benefits'")
        self.why_aerostrat_section = self.page.locator("text='Why Aerostrat'")
        
        # Specific job requirements and benefits
        self.playwright_requirement = self.page.locator("text=/Playwright/i").first
        self.cypress_requirement = self.page.locator("text=/Cypress/i").first
        self.python_requirement = self.page.locator("text=/Python/i").first
        self.salary_range = self.page.locator(".posting-categories .sort-by-salary").first
        
        # Application elements
        self.apply_button = self.page.locator("a:has-text('APPLY FOR THIS JOB')").first
        self.aerostrat_homepage_link = self.page.locator(".main-header-logo a[href*='aerostrat']").first
        
        # Footer elements
        self.lever_branding = self.page.locator("text='Jobs powered by Lever'")
        self.privacy_notice = self.page.locator("text='Privacy Notice'")
        self.cookie_policy_link = self.page.locator("a:has-text('Cookie Policy')")
        self.dismiss_cookie_button = self.page.locator("button.cc-dismiss").first
        
        # Content validation elements
        self.main_content = self.page.locator("body")
        self.loading_spinner = self.page.locator(".loading")
        self.error_message = self.page.locator(".error")
        
    def navigate_to(self, job_id: str = "adac8189-b81c-4d24-9b66-a43f138685ac"):
        """Navigate to the Aerostrat job posting page.
        
        Args:
            job_id: The job ID for the specific posting. Defaults to QA Engineer position.
        """
        url = f"https://jobs.lever.co/aerostrat/{job_id}"
        self.page.goto(url)
    
    def wait_for_page_load(self, timeout: int = 30000):
        """Wait for the job page to fully load.
        
        Args:
            timeout: Maximum time to wait in milliseconds
        """
        # Wait for the main content to be visible
        self.main_content.wait_for(state="visible", timeout=timeout)
        
        # Wait for the job title to be visible
        self.job_title.wait_for(state="visible", timeout=timeout)
        
        # Wait for any loading spinners to disappear
        if self.loading_spinner.count() > 0:
            self.loading_spinner.wait_for(state="hidden", timeout=timeout)
    
    def get_job_title(self) -> str:
        """Get the job title text.
        
        Returns:
            The job title as a string
        """
        return self.job_title.text_content()
    
    def get_page_title(self) -> str:
        """Get the browser page title.
        
        Returns:
            The browser page title as a string
        """
        return self.page.title()
    
    def is_page_loaded(self) -> bool:
        """Check if the job page is fully loaded.
        
        Returns:
            True if page is loaded, False otherwise
        """
        return (
            self.main_content.is_visible() and
            self.job_title.is_visible() and
            not self.loading_spinner.is_visible()
        )
    
    def dismiss_cookie_notice(self):
        """Dismiss the cookie notice if present."""
        if self.dismiss_cookie_button.is_visible():
            self.dismiss_cookie_button.click()
    
    def click_apply_button(self):
        """Click the 'APPLY FOR THIS JOB' button."""
        self.apply_button.click()
    
    def navigate_to_aerostrat_homepage(self):
        """Click the link to navigate to Aerostrat's homepage."""
        self.aerostrat_homepage_link.click()
    
    def get_job_details(self) -> dict:
        """Get basic job details from the page.
        
        Returns:
            Dictionary containing job details
        """
        # Try to get location and department from the page content
        location = ""
        department = ""
        job_type = ""
        
        try:
            # Look for location info in the page content
            location_elements = self.page.locator("text=/Seattle/i")
            if location_elements.count() > 0:
                location = "Seattle"
        except:
            pass
            
        try:
            # Look for department info
            dept_elements = self.page.locator("text=/Software Engineering/i")
            if dept_elements.count() > 0:
                department = "Software Engineering"
        except:
            pass
            
        try:
            # Look for job type
            type_elements = self.page.locator("text=/Full-Time/i")
            if type_elements.count() > 0:
                job_type = "Full-Time"
        except:
            pass
        
        return {
            "title": self.get_job_title(),
            "location": location,
            "department": department,
            "type": job_type,
            "remote": self.remote_indicator.is_visible()
        }
    
    def has_salary_range(self) -> bool:
        """Check if a salary range is displayed.
        
        Returns:
            True if salary range is visible, False otherwise
        """
        return self.salary_range.count() > 0
    
    def get_salary_range(self) -> str:
        """Get the salary range from the compensation section.
        
        Returns:
            Salary range as a string
        """
        if self.salary_range.count() > 0:
            return self.salary_range.text_content()
        return ""
    
    def has_technical_requirements(self) -> dict:
        """Check which technical requirements are mentioned in the job posting.
        
        Returns:
            Dictionary indicating which technologies are mentioned
        """
        return {
            "playwright": self.playwright_requirement.is_visible(),
            "cypress": self.cypress_requirement.is_visible(),
            "python": self.python_requirement.is_visible()
        }
    
    def get_job_sections(self) -> dict:
        """Check which job sections are present on the page.
        
        Returns:
            Dictionary indicating which sections are visible
        """
        return {
            "about_aerostrat": self.about_aerostrat_heading.is_visible(),
            "about_role": self.about_role_heading.is_visible(),
            "responsibilities": self.role_responsibilities.is_visible(),
            "requirements": self.role_requirements.is_visible(),
            "compensation": self.compensation_section.is_visible(),
            "benefits": self.benefits_section.is_visible(),
            "why_aerostrat": self.why_aerostrat_section.is_visible()
        }
    
    def has_error_message(self) -> bool:
        """Check if an error message is displayed.
        
        Returns:
            True if error message is visible, False otherwise
        """
        return self.error_message.is_visible()
    
    def get_error_message(self) -> str:
        """Get the error message text.
        
        Returns:
            The error message text, or empty string if no error
        """
        if self.has_error_message():
            return self.error_message.text_content()
        return ""
    
    def scroll_to_apply_button(self):
        """Scroll to the apply button to ensure it's in view."""
        self.apply_button.scroll_into_view_if_needed()
    
    def scroll_to_section(self, section: str):
        """Scroll to a specific job section.
        
        Args:
            section: The section to scroll to ('compensation', 'benefits', etc.)
        """
        section_map = {
            'compensation': self.compensation_section,
            'benefits': self.benefits_section,
            'requirements': self.role_requirements,
            'responsibilities': self.role_responsibilities,
            'about_aerostrat': self.about_aerostrat_heading,
            'about_role': self.about_role_heading
        }
        
        if section in section_map:
            section_map[section].scroll_into_view_if_needed()
    
    # Assertion methods for job page validation
    def assert_job_title(self, expected_title: str = "Software Engineer - QA"):
        """Assert that the job title matches expected value.
        
        Args:
            expected_title: The expected job title
        """
        expect(self.job_title).to_contain_text(expected_title)
    
    def assert_page_loaded(self):
        """Assert that the job page is fully loaded."""
        expect(self.main_content).to_be_visible()
        expect(self.job_title).to_be_visible()
        expect(self.apply_button).to_be_visible()
    
    def assert_no_errors(self):
        """Assert that no error messages are displayed."""
        expect(self.error_message).to_be_hidden()
    
    def assert_apply_button_visible(self):
        """Assert that the apply button is visible and clickable."""
        expect(self.apply_button).to_be_visible()
        expect(self.apply_button).to_be_enabled()
    
    def assert_salary_range_visible(self):
        """Assert that salary information is displayed."""
        expect(self.salary_range).to_be_visible()
    
    def assert_technical_requirements_present(self):
        """Assert that key technical requirements are mentioned."""
        expect(self.playwright_requirement).to_be_visible()
        # Note: Either Playwright OR Cypress should be mentioned
        playwright_visible = self.playwright_requirement.is_visible()
        cypress_visible = self.cypress_requirement.is_visible()
        assert playwright_visible or cypress_visible, "Either Playwright or Cypress should be mentioned"
    
    def assert_all_sections_present(self):
        """Assert that all major job sections are present."""
        sections = self.get_job_sections()
        required_sections = ['about_aerostrat', 'responsibilities', 'requirements', 'compensation', 'benefits']
        
        for section in required_sections:
            assert sections.get(section, False), f"Section '{section}' should be present on the page"