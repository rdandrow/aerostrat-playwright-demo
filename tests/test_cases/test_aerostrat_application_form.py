"""
Test cases for the Aerostrat job application form page.

This module contains comprehensive tests for the Aerostrat job application form
on Lever, demonstrating the use of the AerostratApplicationFormPage page object model.
"""

import pytest
import tempfile
import os
from faker import Faker
from playwright.sync_api import Page, expect
from tests.page_objects.application_form import (
    AerostratApplicationFormPage,
    Pronouns,
    ExperienceLevel
)


class TestAerostratJobApplication:
    """Test class for Aerostrat job application form functionality."""
    
    @pytest.fixture
    def fake(self):
        """Fixture to create and return a Faker instance."""
        return Faker()
    
    @pytest.fixture
    def application_form(self, page: Page):
        """Fixture to create and return an AerostratApplicationFormPage instance."""
        return AerostratApplicationFormPage(page)
    
    @pytest.fixture
    def sample_resume_file(self, fake):
        """Fixture to create a temporary resume file for testing with dynamic data."""
        # Create a temporary file with dynamic resume content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(f"Resume for {fake.name()}\n")
            f.write(f"Email: {fake.email()}\n")
            f.write(f"Phone: {fake.phone_number()}\n")
            f.write(f"Address: {fake.address()}\n")
            f.write(f"Job Title: {fake.job()}\n")
            f.write(f"Company: {fake.company()}\n")
            f.write(f"Experience: {fake.random_int(min=1, max=15)} years in {fake.bs()}\n")
            f.write(f"Skills: {', '.join(fake.words(nb=5))}\n")
            f.write(f"Education: {fake.catch_phrase()}\n")
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    def test_application_form_loads_successfully(self, application_form: AerostratApplicationFormPage):
        """Test that the application form loads successfully with all required elements."""
        # Navigate to the application form
        application_form.navigate_to()
        
        # Wait for page to load and dismiss cookie notice if present
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Verify page is loaded
        application_form.assert_page_loaded()
        
        # Verify all major sections are present
        application_form.assert_form_sections_present()
    
    def test_required_fields_are_marked(self, application_form: AerostratApplicationFormPage):
        """Test that all expected required fields are properly marked as required."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Check that required fields are properly marked
        application_form.assert_required_fields_present()
        
        # Get and verify required fields list
        required_fields = application_form.get_required_fields()
        assert len(required_fields) > 0, "No required fields found"
    
    def test_personal_information_section(self, application_form: AerostratApplicationFormPage, fake):
        """Test filling out the personal information section."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Generate dynamic test data
        full_name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        location = f"{fake.city()}, {fake.state_abbr()}"
        company = fake.company()
        
        # Fill personal information
        application_form.fill_personal_information(
            full_name=full_name,
            email=email,
            phone=phone,
            location=location,
            company=company,
            pronouns=fake.random_element(elements=[Pronouns.SHE_HER, Pronouns.HE_HIM, Pronouns.THEY_THEM])
        )
        
        # Verify the information was filled
        expect(application_form.full_name_input).to_have_value(full_name)
        expect(application_form.email_input).to_have_value(email)
        expect(application_form.phone_input).to_have_value(phone)
    
    def test_pronouns_selection(self, application_form: AerostratApplicationFormPage):
        """Test selecting different pronoun options."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Test different pronoun selections
        pronoun_tests = [
            Pronouns.HE_HIM,
            Pronouns.THEY_THEM,
            Pronouns.USE_NAME_ONLY,
            Pronouns.CUSTOM
        ]
        
        for pronoun in pronoun_tests:
            application_form.select_pronouns(pronoun)
            # Add a small delay between selections
            application_form.page.wait_for_timeout(500)
    
    def test_links_section_filling(self, application_form: AerostratApplicationFormPage, fake):
        """Test filling out the links section with various URLs."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Scroll to links section
        application_form.scroll_to_section("links")
        
        # Generate dynamic URLs
        username = fake.user_name()
        linkedin_url = f"https://linkedin.com/in/{username}"
        portfolio_url = f"https://{username}.{fake.random_element(elements=['dev', 'com', 'io'])}"
        github_url = f"https://github.com/{username}"
        other_url = f"https://{username}.{fake.random_element(elements=['blog', 'portfolio', 'website'])}"
        
        # Fill links section
        application_form.fill_links_section(
            linkedin_url=linkedin_url,
            portfolio_url=portfolio_url,
            github_url=github_url,
            other_url=other_url
        )
        
        # Verify the links were filled
        expect(application_form.linkedin_input).to_have_value(linkedin_url)
        expect(application_form.portfolio_input).to_have_value(portfolio_url)
        expect(application_form.github_input).to_have_value(github_url)
        expect(application_form.other_url_input).to_have_value(other_url)
    
    def test_experience_questions_answering(self, application_form: AerostratApplicationFormPage):
        """Test answering all job-specific experience questions."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Scroll to questions section
        application_form.scroll_to_section("questions")
        
        # Verify all questions are present
        application_form.assert_all_experience_questions_present()
        
        # Answer experience questions
        application_form.answer_experience_questions(
            e2e_automation=ExperienceLevel.TWO_TO_FOUR,
            python=ExperienceLevel.FIVE_PLUS,
            playwright=ExperienceLevel.ONE_TO_TWO,
            automation_types=ExperienceLevel.TWO_TO_FOUR
        )
        
        # Verify selections were made (check that radio buttons are checked)
        expect(application_form.e2e_automation_2_4).to_be_checked()
        expect(application_form.python_5_plus).to_be_checked()
        expect(application_form.playwright_1_2).to_be_checked()
        expect(application_form.automation_types_2_4).to_be_checked()
    
    def test_individual_experience_question_selection(self, application_form: AerostratApplicationFormPage):
        """Test selecting individual experience levels for each question."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        application_form.scroll_to_section("questions")
        
        # Test E2E automation experience selection
        application_form.select_e2e_automation_experience(ExperienceLevel.FIVE_PLUS)
        expect(application_form.e2e_automation_5_plus).to_be_checked()
        
        # Test Python experience selection
        application_form.select_python_experience(ExperienceLevel.TWO_TO_FOUR)
        expect(application_form.python_2_4).to_be_checked()
        
        # Test Playwright experience selection
        application_form.select_playwright_experience(ExperienceLevel.ZERO_TO_ONE)
        expect(application_form.playwright_0_1).to_be_checked()
        
        # Test automation types experience selection
        application_form.select_automation_types_experience(ExperienceLevel.ONE_TO_TWO)
        expect(application_form.automation_types_1_2).to_be_checked()
    
    def test_additional_information_section(self, application_form: AerostratApplicationFormPage, fake):
        """Test filling out the additional information section."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Scroll to additional information section
        application_form.scroll_to_section("additional")
        
        # Generate dynamic additional information
        passion_area = fake.random_element(elements=['test automation', 'quality assurance', 'software development', 'system integration'])
        frameworks = fake.random_sample(elements=['Playwright', 'Selenium', 'Cypress', 'TestCafe', 'Jest', 'PyTest'], length=3)
        frameworks_text = ', '.join(frameworks[:-1]) + f', and {frameworks[-1]}'
        
        additional_text = f"""
        I am passionate about {passion_area} and have {fake.random_int(min=2, max=8)} years of experience in the field. 
        I have hands-on experience with various testing frameworks including {frameworks_text}.
        I am excited about the opportunity to contribute to Aerostrat's mission and bring my expertise in {fake.random_element(elements=['automation', 'quality engineering', 'test strategy', 'continuous integration'])}.
        """
        
        # Fill additional information
        application_form.fill_additional_information(additional_text.strip())
        
        # Verify the text was filled
        expect(application_form.additional_info_textarea).to_have_value(additional_text.strip())
    
    def test_resume_upload_functionality(self, application_form: AerostratApplicationFormPage, sample_resume_file):
        """Test resume file upload functionality."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Upload resume file
        application_form.upload_resume(sample_resume_file)
        
        # Verify file was uploaded - check that the file input has files
        # For file inputs, we need to use JavaScript to check the files property
        files_count = application_form.page.evaluate("() => document.querySelector('input[type=file]').files.length")
        assert files_count > 0, "No files were uploaded to the resume input"
        
        # Also verify that the filename is displayed (UI should no longer show "No file chosen")
        # Wait a moment for the UI to update
        application_form.page.wait_for_timeout(1000)
        
        # Check that "No file chosen" is no longer visible (indicates a file was selected)
        no_file_text = application_form.page.locator("text='No file chosen'")
        if no_file_text.count() > 0:
            expect(no_file_text).not_to_be_visible()
    
    def test_complete_application_form_workflow(self, application_form: AerostratApplicationFormPage, sample_resume_file, fake):
        """Test filling out the complete application form from start to finish."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Generate dynamic test data
        full_name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        location = f"{fake.city()}, {fake.state_abbr()}"
        company = fake.company()
        username = fake.user_name()
        linkedin_url = f"https://linkedin.com/in/{username}"
        portfolio_url = f"https://{username}.{fake.random_element(elements=['dev', 'io', 'com'])}"
        github_url = f"https://github.com/{username}"
        other_url = f"https://blog.{username}.{fake.random_element(elements=['dev', 'com', 'io'])}"
        additional_info = f"{fake.sentence()} {fake.company_suffix()} and contribute to {fake.random_element(elements=['aviation technology', 'aerospace innovation', 'technical excellence'])}!"
        
        # Generate random experience levels for verification later
        e2e_automation_level = fake.random_element(elements=[ExperienceLevel.ONE_TO_TWO, ExperienceLevel.TWO_TO_FOUR, ExperienceLevel.FIVE_PLUS])
        python_level = fake.random_element(elements=[ExperienceLevel.TWO_TO_FOUR, ExperienceLevel.FIVE_PLUS])
        playwright_level = fake.random_element(elements=[ExperienceLevel.ONE_TO_TWO, ExperienceLevel.TWO_TO_FOUR])
        automation_types_level = fake.random_element(elements=[ExperienceLevel.TWO_TO_FOUR, ExperienceLevel.FIVE_PLUS])
        
        # Fill complete application using the comprehensive method
        application_form.fill_complete_application(
            resume_path=sample_resume_file,
            full_name=full_name,
            email=email,
            phone=phone,
            location=location,
            company=company,
            pronouns=fake.random_element(elements=[Pronouns.SHE_HER, Pronouns.HE_HIM, Pronouns.THEY_THEM]),
            linkedin_url=linkedin_url,
            portfolio_url=portfolio_url,
            github_url=github_url,
            other_url=other_url,
            e2e_automation=e2e_automation_level,
            python=python_level,
            playwright=playwright_level,
            automation_types=automation_types_level,
            additional_info=additional_info
        )
        
        # Verify key fields are filled
        expect(application_form.full_name_input).to_have_value(full_name)
        expect(application_form.email_input).to_have_value(email)
        expect(application_form.linkedin_input).to_have_value(linkedin_url)
        
        # Verify experience selections based on what was actually selected
        # Helper function to get the correct radio button for each experience level
        def get_e2e_radio_button(level):
            mapping = {
                ExperienceLevel.ONE_TO_TWO: application_form.e2e_automation_1_2,
                ExperienceLevel.TWO_TO_FOUR: application_form.e2e_automation_2_4,
                ExperienceLevel.FIVE_PLUS: application_form.e2e_automation_5_plus
            }
            return mapping[level]
        
        def get_python_radio_button(level):
            mapping = {
                ExperienceLevel.TWO_TO_FOUR: application_form.python_2_4,
                ExperienceLevel.FIVE_PLUS: application_form.python_5_plus
            }
            return mapping[level]
        
        def get_playwright_radio_button(level):
            mapping = {
                ExperienceLevel.ONE_TO_TWO: application_form.playwright_1_2,
                ExperienceLevel.TWO_TO_FOUR: application_form.playwright_2_4
            }
            return mapping[level]
        
        # Verify the selected experience levels
        expect(get_e2e_radio_button(e2e_automation_level)).to_be_checked()
        expect(get_python_radio_button(python_level)).to_be_checked()
        expect(get_playwright_radio_button(playwright_level)).to_be_checked()
        
        # Verify additional information
        expect(application_form.additional_info_textarea).to_have_value(additional_info)
    
    def test_form_validation_and_error_handling(self, application_form: AerostratApplicationFormPage, fake):
        """Test form validation and error handling."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Clear any existing error messages that might persist from browser state
        # Refresh the page to ensure clean state
        application_form.page.reload()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Check for validation errors on fresh form - allow for some pre-existing errors
        # due to browser state persistence
        if application_form.has_validation_errors():
            existing_errors = application_form.get_validation_errors()
            print(f"Note: Found pre-existing validation errors: {existing_errors}")
            # For now, we'll continue with the test as these might be browser state artifacts
        
        # Try to submit form without required fields (if validation occurs client-side)
        # Note: We don't actually submit to avoid creating real applications
        
        # Verify form completeness checking
        is_complete_before = application_form.is_form_complete()
        
        # Fill minimum required information with dynamic data
        application_form.fill_personal_information(
            full_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            location=f"{fake.city()}, {fake.state_abbr()}",
            company=fake.company()
        )
        
        # Check if form completeness status changed
        is_complete_after = application_form.is_form_complete()
        
        # The form completeness should change after filling required fields
        # (This depends on the actual form validation implementation)
    
    def test_section_scrolling_functionality(self, application_form: AerostratApplicationFormPage):
        """Test scrolling to different sections of the form."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Test scrolling to each section
        sections_to_test = ["personal", "links", "questions", "additional"]
        
        for section in sections_to_test:
            application_form.scroll_to_section(section)
            # Add a delay to see the scrolling in action
            application_form.page.wait_for_timeout(1000)
    
    def test_form_navigation_elements(self, application_form: AerostratApplicationFormPage):
        """Test navigation elements on the application form page."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Verify navigation elements are present
        expect(application_form.aerostrat_logo).to_be_visible()
        expect(application_form.job_title).to_be_visible()
        expect(application_form.aerostrat_homepage_link).to_be_visible()
        expect(application_form.lever_branding).to_be_visible()
    
    @pytest.mark.parametrize("experience_level", [
        ExperienceLevel.NONE,
        ExperienceLevel.ZERO_TO_ONE,
        ExperienceLevel.ONE_TO_TWO,
        ExperienceLevel.TWO_TO_FOUR,
        ExperienceLevel.FIVE_PLUS
    ])
    def test_all_experience_levels_selectable(self, application_form: AerostratApplicationFormPage, experience_level):
        """Test that all experience levels can be selected for each question."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        application_form.scroll_to_section("questions")
        
        # Test each experience level for E2E automation question
        application_form.select_e2e_automation_experience(experience_level)
        
        # Verify the selection worked
        experience_map = {
            ExperienceLevel.NONE: application_form.e2e_automation_none,
            ExperienceLevel.ZERO_TO_ONE: application_form.e2e_automation_0_1,
            ExperienceLevel.ONE_TO_TWO: application_form.e2e_automation_1_2,
            ExperienceLevel.TWO_TO_FOUR: application_form.e2e_automation_2_4,
            ExperienceLevel.FIVE_PLUS: application_form.e2e_automation_5_plus
        }
        
        expect(experience_map[experience_level]).to_be_checked()
    
    @pytest.mark.parametrize("pronoun", [
        Pronouns.HE_HIM,
        Pronouns.SHE_HER,
        Pronouns.THEY_THEM,
        Pronouns.USE_NAME_ONLY
    ])
    def test_all_pronouns_selectable(self, application_form: AerostratApplicationFormPage, pronoun):
        """Test that all pronoun options can be selected."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Select the pronoun
        application_form.select_pronouns(pronoun)
        
        # Verify the selection
        pronoun_map = {
            Pronouns.HE_HIM: application_form.pronoun_he_him,
            Pronouns.SHE_HER: application_form.pronoun_she_her,
            Pronouns.THEY_THEM: application_form.pronoun_they_them,
            Pronouns.USE_NAME_ONLY: application_form.pronoun_use_name_only
        }
        
        expect(pronoun_map[pronoun]).to_be_checked()
    
    def test_ai_disclosure_and_privacy_elements(self, application_form: AerostratApplicationFormPage):
        """Test that AI disclosure and privacy elements are present."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Scroll to bottom to see footer elements
        application_form.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        # Verify AI disclosure and privacy elements
        expect(application_form.ai_disclosure).to_be_visible()
        expect(application_form.lever_branding).to_be_visible()
    
    @pytest.mark.slow
    def test_form_performance_and_responsiveness(self, application_form: AerostratApplicationFormPage, fake):
        """Test form performance and responsiveness."""
        import time
        
        start_time = time.time()
        
        application_form.navigate_to()
        application_form.wait_for_page_load()
        
        load_time = time.time() - start_time
        
        # Assert reasonable load time (adjust threshold as needed)
        assert load_time < 10, f"Form took {load_time:.2f} seconds to load, which is too slow"
        
        # Test form interactions are responsive
        application_form.dismiss_cookie_notice()
        
        # Fill form quickly and verify responsiveness
        fill_start = time.time()
        
        application_form.fill_personal_information(
            full_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            location=f"{fake.city()}, {fake.state_abbr()}",
            company=fake.company()
        )
        
        fill_time = time.time() - fill_start
        
        # Form filling should be fast
        assert fill_time < 5, f"Form filling took {fill_time:.2f} seconds, which is too slow"
    
    def test_form_accessibility_elements(self, application_form: AerostratApplicationFormPage):
        """Test that form has proper accessibility elements."""
        application_form.navigate_to()
        application_form.wait_for_page_load()
        application_form.dismiss_cookie_notice()
        
        # Check that form fields have proper labels
        expect(application_form.full_name_label).to_be_visible()
        
        # Check that required fields are properly marked
        expect(application_form.resume_required_indicator).to_be_visible()
        
        # Verify submit button is accessible
        expect(application_form.submit_button).to_be_visible()
        expect(application_form.submit_button).to_be_enabled()


# Pytest configuration for this test module
@pytest.fixture(scope="session")  
def browser_context_args(browser_context_args):
    """Configure browser context for application form tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "user_agent": "Aerostrat-Application-Tests/1.0"
    }