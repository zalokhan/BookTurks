from django.test import TestCase, Client
from django.core.urlresolvers import reverse

"""
Test case for the Main Home Page
"""


class MainHomeArenaTest(TestCase):
    """
    check if page is available.
    """

    def test_main_home_arena_view(self):
        client = Client()
        response = client.get(reverse('service:main_home'))
        self.assertEqual(200, 200)
