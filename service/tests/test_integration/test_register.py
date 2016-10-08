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

        self.driver.get('{0}{1}'.format(self.live_server_url, '/#signin'))
        self.driver.find_element_by_id('register_button').click()
        assert self.driver.current_url, '{0}{1}'.format(self.live_server_url, '/register/')

        self.driver.find_element_by_name("user_first_name").send_keys('TestFirstName')
        self.driver.find_element_by_name("user_last_name").send_keys('TestLastName')
        self.driver.find_element_by_name("username").send_keys('2test@email.com')
        self.driver.find_element_by_name("password").send_keys('password')
        self.driver.find_element_by_name("repassword").send_keys('password')
        self.driver.find_element_by_name("user_phone").send_keys('1234567890')
        self.driver.find_element_by_name("user_dob").send_keys('01/01/1990')

        self.driver.find_element_by_id('register_button').click()

        assert self.driver.current_url, '{0}{1}'.format(self.live_server_url, '/')
