from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from service.tests.create_user import create_user, context


class UserHomeViewTest(TestCase):
    """
    Test case for the User Home Page
    """

    def test_user_home_view(self):
        """
        Testing the dashboard view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_home'), context)
        self.assertEqual(response.status_code, 200)
