import os

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


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
    capabilities['browserName'] = 'chrome'

    return webdriver.Remote(desired_capabilities=capabilities,
                            command_executor="http://{0}/wd/hub".format(hub_url))


def get_local_driver():
    """
    Returns local web driver
    :return:
    """
    chromedriver_path = settings.BASE_DIR + '/service/tests/chromedrivers/chromedriver'
    if os.path.isfile(chromedriver_path):
        return webdriver.Chrome(chromedriver_path)
    else:
        raise FileNotFoundError("Chromedriver not found. Place file or link in {0}".format(chromedriver_path))


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
            cls.driver = get_sauce_driver(cls.capabilities)
        else:
            cls.driver = get_local_driver()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(SeleniumTests, cls).tearDownClass()
