"""
Aerostrat Job Application Form Page Object Model

This module contains the page object model for the Aerostrat job application form page on Lever,
following Playwright best practices for form automation and validation.
"""

from playwright.sync_api import Page, Locator, expect
from typing import Dict, List, Optional
from enum import Enum


class Pronouns(Enum):
    """Enum for pronoun options."""
    HE_HIM = "He/him"
    SHE_HER = "She/her"
    THEY_THEM = "They/them"
    XE_XEM = "Xe/xem"
    ZE_HIR = "Ze/hir"
    EY_EM = "Ey/em"
    HIR_HIR = "Hir/hir"
    FAE_FAER = "Fae/faer"
    HU_HU = "Hu/hu"
    USE_NAME_ONLY = "Use name only"
    CUSTOM = "Custom"


class ExperienceLevel(Enum):
    """Enum for experience level options."""
    NONE = "None"
    ZERO_TO_ONE = "0-1 year"
    ONE_TO_TWO = "1-2 years"
    TWO_TO_FOUR = "2-4 years"
    FIVE_PLUS = "5+ years"


class AerostratApplicationFormPage:
    """Page Object Model for the Aerostrat job application form on Lever."""
    
    def __init__(self, page: Page):
        """Initialize the AerostratApplicationFormPage.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self._setup_locators()
    
    def _setup_locators(self):
        """Define all locators for the application form elements."""
        
        # Header elements
        self.aerostrat_logo = self.page.locator(".main-header-logo img[alt*='Aerostrat']")
        self.job_title = self.page.locator("h2:has-text('Software Engineer - QA')")
        self.page_heading = self.page.locator("h4:has-text('SUBMIT YOUR APPLICATION')")
        
        # Personal Information Section
        self.resume_upload = self.page.locator("input[type='file']")
        self.attach_resume_button = self.page.locator("button:has-text('ATTACH RESUME/CV')")
        self.resume_required_indicator = self.page.locator("div.application-label:has-text('Resume/CV')")
        
        self.full_name_input = self.page.locator("input[name='name']")
        self.full_name_label = self.page.locator("label:has-text('Full name')")
        
        # Pronouns section
        self.pronouns_section = self.page.locator("text='Pronouns'").locator("..")
        self.pronoun_he_him = self.page.locator("input[value='He/him']")
        self.pronoun_she_her = self.page.locator("input[value='She/her']")
        self.pronoun_they_them = self.page.locator("input[value='They/them']")
        self.pronoun_xe_xem = self.page.locator("input[value='Xe/xem']")
        self.pronoun_ze_hir = self.page.locator("input[value='Ze/hir']")
        self.pronoun_ey_em = self.page.locator("input[value='Ey/em']")
        self.pronoun_hir_hir = self.page.locator("input[value='Hir/hir']")
        self.pronoun_fae_faer = self.page.locator("input[value='Fae/faer']")
        self.pronoun_hu_hu = self.page.locator("input[value='Hu/hu']")
        self.pronoun_use_name_only = self.page.locator("input[value='Use name only']")
        self.pronoun_custom = self.page.locator("input[value='Custom']")
        
        self.email_input = self.page.locator("input[name='email']")
        self.phone_input = self.page.locator("input[name='phone']")
        self.current_location_input = self.page.locator("input[name='location'][type='text']")
        self.current_company_input = self.page.locator("input[data-qa='org-input']")
        
        # Links Section
        self.links_heading = self.page.locator("h4:has-text('LINKS')")
        self.linkedin_input = self.page.locator("input[name='urls[LinkedIn]'][type='text']")
        self.portfolio_input = self.page.locator("input[name*='portfolio' i]")
        self.github_input = self.page.locator("input[name*='github' i]")
        self.other_url_input = self.page.locator("input[name*='other' i]")
        
        # Job-Specific Questions Section
        self.questions_heading = self.page.locator("h4:has-text('SOFTWARE ENGINEER - QA QUESTIONS')")
        
        # Experience questions - E2E automation (first question - use nth)
        self.e2e_automation_question = self.page.locator("text='How many years of work experience do you have developing E2E test automation?'")
        self.e2e_automation_none = self.page.locator("input[value='None']").nth(0)
        self.e2e_automation_0_1 = self.page.locator("input[value='0-1 year']").nth(0)
        self.e2e_automation_1_2 = self.page.locator("input[value='1-2 years']").nth(0)
        self.e2e_automation_2_4 = self.page.locator("input[value='2-4 years']").nth(0)
        self.e2e_automation_5_plus = self.page.locator("input[value='5+ years']").nth(0)
        
        # Experience questions - Python (second question - use nth 1)
        self.python_question = self.page.locator("text='How many years of direct work experience do you have developing code in Python?'")
        self.python_none = self.page.locator("input[value='None']").nth(1)
        self.python_0_1 = self.page.locator("input[value='0-1 year']").nth(1)
        self.python_1_2 = self.page.locator("input[value='1-2 years']").nth(1)
        self.python_2_4 = self.page.locator("input[value='2-4 years']").nth(1)
        self.python_5_plus = self.page.locator("input[value='5+ years']").nth(1)
        
        # Experience questions - Playwright (third question - use nth 2)
        self.playwright_question = self.page.locator("text='How many years of direct work experience do you have developing E2E tests with Playwright?'")
        self.playwright_none = self.page.locator("input[value='None']").nth(2)
        self.playwright_0_1 = self.page.locator("input[value='0-1 year']").nth(2)
        self.playwright_1_2 = self.page.locator("input[value='1-2 years']").nth(2)
        self.playwright_2_4 = self.page.locator("input[value='2-4 years']").nth(2)
        self.playwright_5_plus = self.page.locator("input[value='5+ years']").nth(2)
        
        # Experience questions - Different types of automated tests (fourth question - use nth 3)
        self.automation_types_description = self.page.locator("div.text:has-text('How many years of experience do you have developing different types of automated tests (i.e. API, Security, Performance, etc.)?')")
        self.automation_types_none = self.page.locator("input[value='None']").nth(3)
        self.automation_types_0_1 = self.page.locator("input[value='0-1 year']").nth(3)
        self.automation_types_1_2 = self.page.locator("input[value='1-2 years']").nth(3)
        self.automation_types_2_4 = self.page.locator("input[value='2-4 years']").nth(3)
        self.automation_types_5_plus = self.page.locator("input[value='5+ years']").nth(3)
        
        # Additional Information Section
        self.additional_info_heading = self.page.locator("h4:has-text('ADDITIONAL INFORMATION')")
        self.additional_info_textarea = self.page.locator("textarea")
        
        # Form submission and navigation
        self.submit_button = self.page.locator("button:has-text('SUBMIT APPLICATION')")
        self.aerostrat_homepage_link = self.page.locator("img[alt='Aerostrat logo']")
        
        # Footer elements
        self.ai_disclosure = self.page.locator("p:has-text('We may use artificial intelligence (AI) tools to support parts of the hiring process')")
        self.lever_branding = self.page.locator("a[href='https://www.lever.co/job-seeker-support/']")
        
        # Cookie and privacy elements
        self.cookie_banner = self.page.locator("text='Privacy Notice'")
        self.dismiss_cookie_button = self.page.locator("button.cc-dismiss").first
        
        # Form validation elements
        self.required_field_indicators = self.page.locator("text='✱'")
        self.error_messages = self.page.locator(".error-message, .field-error, .validation-error, [class*='error']")
        
        # Loading and status elements
        self.loading_spinner = self.page.locator(".loading")
        self.success_message = self.page.locator(".success-message")
    
    def navigate_to(self, job_id: str = "2cce6cc2-dcdd-4562-af4d-8eb6afd5b281"):
        """Navigate to the Aerostrat job application form page.
        
        Args:
            job_id: The job ID for the specific posting. Defaults to QA Engineer position.
        """
        url = f"https://jobs.lever.co/aerostrat/{job_id}/apply"
        self.page.goto(url)
    
    def wait_for_page_load(self, timeout: int = 30000):
        """Wait for the application form page to fully load.
        
        Args:
            timeout: Maximum time to wait in milliseconds
        """
        # Wait for the main form elements to be visible
        self.page_heading.wait_for(state="visible", timeout=timeout)
        self.full_name_input.wait_for(state="visible", timeout=timeout)
        self.submit_button.wait_for(state="visible", timeout=timeout)
        
        # Wait for any loading spinners to disappear
        if self.loading_spinner.is_visible():
            self.loading_spinner.wait_for(state="hidden", timeout=timeout)
    
    def dismiss_cookie_notice(self):
        """Dismiss the cookie notice if present."""
        if self.dismiss_cookie_button.is_visible():
            self.dismiss_cookie_button.click()
    
    def upload_resume(self, file_path: str):
        """Upload a resume file.
        
        Args:
            file_path: Path to the resume file to upload
        """
        self.resume_upload.set_input_files(file_path)
    
    def fill_personal_information(self, 
                                full_name: str,
                                email: str,
                                phone: str,
                                location: str,
                                company: str,
                                pronouns: Optional[Pronouns] = None):
        """Fill in the personal information section.
        
        Args:
            full_name: Applicant's full name
            email: Email address
            phone: Phone number
            location: Current location
            company: Current company
            pronouns: Preferred pronouns (optional)
        """
        self.full_name_input.fill(full_name)
        self.email_input.fill(email)
        self.phone_input.fill(phone)
        self.current_location_input.fill(location)
        self.current_company_input.fill(company)
        
        if pronouns:
            self.select_pronouns(pronouns)
    
    def select_pronouns(self, pronouns: Pronouns):
        """Select preferred pronouns.
        
        Args:
            pronouns: The pronoun option to select
        """
        pronoun_map = {
            Pronouns.HE_HIM: self.pronoun_he_him,
            Pronouns.SHE_HER: self.pronoun_she_her,
            Pronouns.THEY_THEM: self.pronoun_they_them,
            Pronouns.XE_XEM: self.pronoun_xe_xem,
            Pronouns.ZE_HIR: self.pronoun_ze_hir,
            Pronouns.EY_EM: self.pronoun_ey_em,
            Pronouns.HIR_HIR: self.pronoun_hir_hir,
            Pronouns.FAE_FAER: self.pronoun_fae_faer,
            Pronouns.HU_HU: self.pronoun_hu_hu,
            Pronouns.USE_NAME_ONLY: self.pronoun_use_name_only,
            Pronouns.CUSTOM: self.pronoun_custom
        }
        
        if pronouns in pronoun_map:
            pronoun_map[pronouns].check()
    
    def fill_links_section(self, 
                          linkedin_url: Optional[str] = None,
                          portfolio_url: Optional[str] = None,
                          github_url: Optional[str] = None,
                          other_url: Optional[str] = None):
        """Fill in the links section.
        
        Args:
            linkedin_url: LinkedIn profile URL (optional)
            portfolio_url: Portfolio website URL (optional)
            github_url: GitHub profile URL (optional)
            other_url: Other relevant URL (optional)
        """
        if linkedin_url:
            self.linkedin_input.fill(linkedin_url)
        if portfolio_url:
            self.portfolio_input.fill(portfolio_url)
        if github_url:
            self.github_input.fill(github_url)
        if other_url:
            self.other_url_input.fill(other_url)
    
    def answer_experience_questions(self,
                                   e2e_automation: ExperienceLevel,
                                   python: ExperienceLevel,
                                   playwright: ExperienceLevel,
                                   automation_types: ExperienceLevel):
        """Answer the job-specific experience questions.
        
        Args:
            e2e_automation: Years of E2E automation experience
            python: Years of Python experience
            playwright: Years of Playwright experience
            automation_types: Years of different automation types experience
        """
        self.select_e2e_automation_experience(e2e_automation)
        self.select_python_experience(python)
        self.select_playwright_experience(playwright)
        self.select_automation_types_experience(automation_types)
    
    def select_e2e_automation_experience(self, level: ExperienceLevel):
        """Select E2E automation experience level.
        
        Args:
            level: Experience level to select
        """
        experience_map = {
            ExperienceLevel.NONE: self.e2e_automation_none,
            ExperienceLevel.ZERO_TO_ONE: self.e2e_automation_0_1,
            ExperienceLevel.ONE_TO_TWO: self.e2e_automation_1_2,
            ExperienceLevel.TWO_TO_FOUR: self.e2e_automation_2_4,
            ExperienceLevel.FIVE_PLUS: self.e2e_automation_5_plus
        }
        
        if level in experience_map:
            experience_map[level].check()
    
    def select_python_experience(self, level: ExperienceLevel):
        """Select Python experience level.
        
        Args:
            level: Experience level to select
        """
        experience_map = {
            ExperienceLevel.NONE: self.python_none,
            ExperienceLevel.ZERO_TO_ONE: self.python_0_1,
            ExperienceLevel.ONE_TO_TWO: self.python_1_2,
            ExperienceLevel.TWO_TO_FOUR: self.python_2_4,
            ExperienceLevel.FIVE_PLUS: self.python_5_plus
        }
        
        if level in experience_map:
            experience_map[level].check()
    
    def select_playwright_experience(self, level: ExperienceLevel):
        """Select Playwright experience level.
        
        Args:
            level: Experience level to select
        """
        experience_map = {
            ExperienceLevel.NONE: self.playwright_none,
            ExperienceLevel.ZERO_TO_ONE: self.playwright_0_1,
            ExperienceLevel.ONE_TO_TWO: self.playwright_1_2,
            ExperienceLevel.TWO_TO_FOUR: self.playwright_2_4,
            ExperienceLevel.FIVE_PLUS: self.playwright_5_plus
        }
        
        if level in experience_map:
            experience_map[level].check()
    
    def select_automation_types_experience(self, level: ExperienceLevel):
        """Select automation types experience level.
        
        Args:
            level: Experience level to select
        """
        experience_map = {
            ExperienceLevel.NONE: self.automation_types_none,
            ExperienceLevel.ZERO_TO_ONE: self.automation_types_0_1,
            ExperienceLevel.ONE_TO_TWO: self.automation_types_1_2,
            ExperienceLevel.TWO_TO_FOUR: self.automation_types_2_4,
            ExperienceLevel.FIVE_PLUS: self.automation_types_5_plus
        }
        
        if level in experience_map:
            experience_map[level].check()
    
    def fill_additional_information(self, text: str):
        """Fill in the additional information section.
        
        Args:
            text: Additional information to include
        """
        self.additional_info_textarea.fill(text)
    
    def submit_application(self):
        """Submit the job application form."""
        self.submit_button.click()
    
    def scroll_to_section(self, section: str):
        """Scroll to a specific form section.
        
        Args:
            section: The section to scroll to ('personal', 'links', 'questions', 'additional')
        """
        section_map = {
            'personal': self.page_heading,
            'links': self.links_heading,
            'questions': self.questions_heading,
            'additional': self.additional_info_heading
        }
        
        if section in section_map:
            section_map[section].scroll_into_view_if_needed()
    
    def get_required_fields(self) -> List[str]:
        """Get a list of required field labels.
        
        Returns:
            List of required field names
        """
        required_fields = []
        for element in self.required_field_indicators.all():
            parent_text = element.locator("..").text_content()
            if parent_text:
                required_fields.append(parent_text.replace('✱', '').strip())
        return required_fields
    
    def has_validation_errors(self) -> bool:
        """Check if there are validation errors on the form.
        
        Returns:
            True if validation errors are present, False otherwise
        """
        return self.error_messages.count() > 0
    
    def get_validation_errors(self) -> List[str]:
        """Get all validation error messages.
        
        Returns:
            List of validation error messages
        """
        errors = []
        for error in self.error_messages.all():
            error_text = error.text_content()
            if error_text:
                errors.append(error_text.strip())
        return errors
    
    def is_form_complete(self) -> bool:
        """Check if all required fields are filled.
        
        Returns:
            True if form appears complete, False otherwise
        """
        # Check if submit button is enabled (basic completeness check)
        return self.submit_button.is_enabled()
    
    def fill_complete_application(self,
                                 resume_path: str,
                                 full_name: str,
                                 email: str,
                                 phone: str,
                                 location: str,
                                 company: str,
                                 pronouns: Optional[Pronouns] = None,
                                 linkedin_url: Optional[str] = None,
                                 portfolio_url: Optional[str] = None,
                                 github_url: Optional[str] = None,
                                 other_url: Optional[str] = None,
                                 e2e_automation: ExperienceLevel = ExperienceLevel.TWO_TO_FOUR,
                                 python: ExperienceLevel = ExperienceLevel.TWO_TO_FOUR,
                                 playwright: ExperienceLevel = ExperienceLevel.ONE_TO_TWO,
                                 automation_types: ExperienceLevel = ExperienceLevel.TWO_TO_FOUR,
                                 additional_info: Optional[str] = None):
        """Fill out the complete application form with provided information.
        
        Args:
            resume_path: Path to resume file
            full_name: Applicant's full name
            email: Email address
            phone: Phone number
            location: Current location
            company: Current company
            pronouns: Preferred pronouns (optional)
            linkedin_url: LinkedIn profile URL (optional)
            portfolio_url: Portfolio website URL (optional)
            github_url: GitHub profile URL (optional)
            other_url: Other relevant URL (optional)
            e2e_automation: E2E automation experience level
            python: Python experience level
            playwright: Playwright experience level
            automation_types: Automation types experience level
            additional_info: Additional information text (optional)
        """
        # Upload resume
        self.upload_resume(resume_path)
        
        # Fill personal information
        self.fill_personal_information(full_name, email, phone, location, company, pronouns)
        
        # Fill links section
        self.fill_links_section(linkedin_url, portfolio_url, github_url, other_url)
        
        # Answer experience questions
        self.answer_experience_questions(e2e_automation, python, playwright, automation_types)
        
        # Fill additional information if provided
        if additional_info:
            self.fill_additional_information(additional_info)
    
    # Assertion methods for form validation
    def assert_page_loaded(self):
        """Assert that the application form page is fully loaded."""
        expect(self.page_heading).to_be_visible()
        expect(self.full_name_input).to_be_visible()
        expect(self.submit_button).to_be_visible()
    
    def assert_required_fields_present(self):
        """Assert that all expected required fields are marked as required."""
        required_fields = self.get_required_fields()
        expected_required = ["Resume/CV", "Full name", "Email", "Phone", "Current location", "Current company"]
        
        for field in expected_required:
            assert any(field in req_field for req_field in required_fields), f"Required field '{field}' not found"
    
    def assert_no_validation_errors(self):
        """Assert that no validation errors are present."""
        assert not self.has_validation_errors(), f"Validation errors found: {self.get_validation_errors()}"
    
    def assert_form_sections_present(self):
        """Assert that all major form sections are visible."""
        expect(self.page_heading).to_be_visible()
        expect(self.links_heading).to_be_visible()
        expect(self.questions_heading).to_be_visible()
        expect(self.additional_info_heading).to_be_visible()
    
    def assert_submit_button_enabled(self):
        """Assert that the submit button is enabled (form is ready for submission)."""
        expect(self.submit_button).to_be_enabled()
    
    def assert_all_experience_questions_present(self):
        """Assert that all job-specific experience questions are visible."""
        expect(self.e2e_automation_question).to_be_visible()
        expect(self.python_question).to_be_visible()
        expect(self.playwright_question).to_be_visible()
        expect(self.automation_types_description).to_be_visible()
    
    def clear_form_errors(self):
        """Attempt to clear any visible form error messages."""
        # This method can be used to dismiss error messages if they have close buttons
        # or to refresh the page to clear persistent errors
        error_close_buttons = self.page.locator(".error-close, .alert-close, [aria-label='close']")
        if error_close_buttons.count() > 0:
            for button in error_close_buttons.all():
                if button.is_visible():
                    button.click()
    
    def refresh_form(self):
        """Refresh the form page to clear any persistent state."""
        self.page.reload()
        self.wait_for_page_load()
        self.dismiss_cookie_notice()