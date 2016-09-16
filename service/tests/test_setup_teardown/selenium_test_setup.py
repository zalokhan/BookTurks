import os

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver


def get_sauce_driver(capabilities):
    """
    Returns web driver for sauce tests
    :return:
    """
    username = settings.SAUCE_USERNAME
    access_key = settings.SAUCE_ACCESS_KEY
    hub_url = "{0}:{1}@ondemand.saucelabs.com:80".format(username, access_key)

    capabilities['tunnel-identifier'] = os.environ["TRAVIS_JOB_NUMBER"]
    capabilities['build'] = os.environ['TRAVIS_BUILD_NUMBER']
    capabilities['tags'] = [os.environ['TRAVIS_PYTHON_VERSION'], 'CI']
    capabilities['browserName'] = 'firefox'

    return webdriver.Remote(desired_capabilities=capabilities,
                            command_executor="http://{0}/wd/hub".format(hub_url))


def get_local_driver():
    """
    Returns local web driver
    :return:
    """
    if 'TRAVIS' in os.environ:
        return WebDriver()
    return webdriver.Chrome(settings.BASE_DIR + '/service/tests/chromedrivers/chromedriver_mac64')


class SeleniumTests(StaticLiveServerTestCase):
    """
    Base setup and tear down for integration tests.
    Distribute into different files if integration tests grow.
    """

    @classmethod
    def setUpClass(cls):
        super(SeleniumTests, cls).setUpClass()
        cls.capabilities = dict()

        if settings.SAUCE_TEST and 'TRAVIS' in os.environ:
            cls.selenium = get_sauce_driver(cls.capabilities)
        else:
            cls.selenium = get_local_driver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()
