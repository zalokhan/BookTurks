import time

from django.contrib.auth.models import User
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from service.bookturks.user.UserProfileTools import UserProfileTools
from service.tests.constants_models import mock_user_model
from service.tests.test_setup_teardown.selenium_test_setup import SeleniumTests


class QuizCreateTests(SeleniumTests):
    """
    Testing creating and deleting quiz functionality
    """

    def test_create_quiz(self):
        """
        tests the create quiz functionality
        :return:
        """

        User.objects.create_user(username='test@email.com', email='test@email.com', password='password')
        mock_user_model.save()

        self.driver.get('{0}{1}'.format(self.live_server_url, '/'))
        self.driver.find_element_by_name("username").send_keys('test@email.com')
        self.driver.find_element_by_name("password").send_keys('password')
        self.driver.find_element_by_id('login_form').submit()

        self.driver.find_element_by_id("sidebar_parent_quiz").click()
        # Wait for drop down to populate
        WebDriverWait(driver=self.driver, timeout=5).until(
            expected_conditions.visibility_of_element_located((By.ID, "sidebar_quiz_init"))
        )

        self.driver.find_element_by_id("sidebar_quiz_init").click()
        self.driver.find_element_by_name("quiz_name").send_keys("mock_quiz")
        self.driver.find_element_by_name("quiz_description").send_keys("mock_description")
        self.driver.find_element_by_id("quiz_init_form").submit()

        # Drag and Drop
        action = ActionChains(self.driver)
        draggable_radio_group = self.driver.find_element_by_class_name("icon-radio-group")
        dragging_destination_box = self.driver.find_element_by_class_name("ui-sortable")
        action.drag_and_drop(draggable_radio_group, dragging_destination_box)
        action.move_to_element(self.driver.find_element_by_id("frmb-0-stage-wrap"))
        action.perform()

        # Edit properties of the element
        # Wait for javascript to animate movement of box
        WebDriverWait(driver=self.driver, timeout=10).until(
            expected_conditions.visibility_of_element_located((By.ID, "frmb-0-fld-1-edit"))
        )
        # time.sleep(0.3)
        self.driver.find_element_by_id("frmb-0-fld-1-edit").click()
        # Wait for edit button to open dropdown
        WebDriverWait(driver=self.driver, timeout=10).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "close-field"))
        )
        self.driver.find_element_by_class_name("close-field").click()
        # Submit quiz
        self.driver.find_element_by_id("frmb-0-submit").click()

        # Mark answer for answer key
        self.driver.find_elements_by_css_selector("input[type=radio][value=option-1]")[0].click()
        self.driver.find_element_by_css_selector("button[type=submit]").click()

        # Check myquiz
        self.driver.find_element_by_id("sidebar_parent_quiz").click()
        self.driver.find_element_by_id("sidebar_myquiz").click()
        # Try deleting
        self.driver.find_element_by_css_selector("button[data-id=testemailcommockquiz]").click()
        # Dismiss deletion
        # Wait for javascript to animate modal
        WebDriverWait(driver=self.driver, timeout=10).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "button[type=button][data-dismiss=modal]")
            )
        )
        # time.sleep(0.3)
        self.driver.find_element_by_css_selector("button[type=button][data-dismiss=modal]").click()

        time.sleep(0.3)  # Wait for modal to fade away.
        # Delete quiz
        self.driver.find_element_by_css_selector("button[data-id=testemailcommockquiz]").click()
        # Wait for javascript to animate modal
        WebDriverWait(driver=self.driver, timeout=10).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "button[type=submit]")
            )
        )
        # time.sleep(0.3)
        self.driver.find_element_by_css_selector("button[type=submit]").click()

        user_profile_tools = UserProfileTools()
        user_profile_tools.delete_profile_from_storage('test@email.com')
