from service.tests.test_setup_teardown.selenium_test_setup import SeleniumTests


class RegisterTests(SeleniumTests):
    """
    Testing Registering a new account and logging in functionality
    """

    def test_register(self):
        """
        tests the registering functionality
        :return:
        """

        self.selenium.get('{0}{1}'.format(self.live_server_url, '/#signin'))
        self.selenium.find_element_by_id('register_button').click()
        assert self.selenium.current_url, '{0}{1}'.format(self.live_server_url, '/register/')

        user_first_name_input = self.selenium.find_element_by_name("user_first_name")
        user_first_name_input.send_keys('TestFirstName')
        user_last_name_input = self.selenium.find_element_by_name("user_last_name")
        user_last_name_input.send_keys('TestLastName')
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('2test@email.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('password')
        repassword_input = self.selenium.find_element_by_name("repassword")
        repassword_input.send_keys('password')
        user_phone_input = self.selenium.find_element_by_name("user_phone")
        user_phone_input.send_keys('1234567890')
        user_dob_input = self.selenium.find_element_by_name("user_dob")
        user_dob_input.send_keys('01/01/1990')
        self.selenium.find_element_by_id('register_button').click()

        assert self.selenium.current_url, '{0}{1}'.format(self.live_server_url, '/')
