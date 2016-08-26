from django.contrib.auth.models import User

from service.bookturks.user.UserProfileTools import UserProfileTools
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

        self.selenium.get('{0}{1}'.format(self.live_server_url, '/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test@email.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('password')
        self.selenium.find_element_by_id('login_form').submit()

        assert self.selenium.current_url, '{0}{1}'.format(self.live_server_url, '/home/')

        self.selenium.find_element_by_id('navbar_dropdown').click()
        self.selenium.find_element_by_id('user_logout').click()
        assert self.selenium.current_url, '{0}{1}'.format(self.live_server_url, '/')

        # Repeat to cover branch when user profile is created and present and has to be fetched.
        self.selenium.get('{0}{1}'.format(self.live_server_url, '/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test@email.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('password')
        self.selenium.find_element_by_id('login_form').submit()
        self.selenium.find_element_by_id('navbar_dropdown').click()
        self.selenium.find_element_by_id('user_logout').click()

        user_profile_tools = UserProfileTools()
        user_profile_tools.delete_profile_from_storage('test@email.com')
