from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class UserHomeViewTest(TestCase):
    """
    Test case for the Main Home Page
    """

    def test_main_home_view(self):
        """
        Testing the main home view
        :return:
        """
        client = Client()
        response = client.get(reverse('service:user_home'))
        # TODO: Fix this.
        self.assertEqual(response.status_code, 302)
