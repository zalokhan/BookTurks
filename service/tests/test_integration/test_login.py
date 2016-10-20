from django.contrib.auth.models import User

from service.bookturks.storage_handlers import UserProfileStorageHandler
from service.tests.constants_models import mock_user_model
from service.tests.test_setup_teardown.selenium_test_setup import SeleniumTests


class LoginTests(SeleniumTests):
    """
    Testing loging in and loging out functionality
    """

    def test_login(self):
        """
        tests the login functionality
        :return:
        """

        User.objects.create_user(username='test@email.com', email='test@email.com', password='password')
        mock_user_model.save()

        self.driver.get('{0}{1}'.format(self.live_server_url, '/'))
        self.driver.find_element_by_name("username").send_keys('test@email.com')
        self.driver.find_element_by_name("password").send_keys('password')
        self.driver.find_element_by_id('login_form').submit()

        assert self.driver.current_url, '{0}{1}'.format(self.live_server_url, '/home/')

        self.driver.find_element_by_id('navbar_dropdown').click()
        self.driver.find_element_by_id('user_logout').click()
        assert self.driver.current_url, '{0}{1}'.format(self.live_server_url, '/')

        # Repeat to cover branch when user profile is created and present and has to be fetched.
        self.driver.get('{0}{1}'.format(self.live_server_url, '/'))
        self.driver.find_element_by_name("username").send_keys('test@email.com')
        self.driver.find_element_by_name("password").send_keys('password')
        self.driver.find_element_by_id('login_form').submit()
        # Clicking the logout button
        self.driver.find_element_by_id('navbar_dropdown').click()
        self.driver.find_element_by_id('user_logout').click()

        user_profile_storage_handler = UserProfileStorageHandler()
        user_profile_storage_handler.delete_profile_from_storage('test@email.com')
