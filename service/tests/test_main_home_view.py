from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class MainHomeViewTest(TestCase):
    """
    Test case for the Main Home Page
    """

    def test_main_home_view(self):
        """
        Testing the main home view
        :return:
        """
        client = Client()
        response = client.get(reverse('service:main_home'))
        self.assertEqual(response.status_code, 200)
