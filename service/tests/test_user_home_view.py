from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User


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
        context = {
            'username': 'test@email.com',
            'user_first_name': 'testfirstname',
            'user_last_name': 'testlastname',
            'user_phone': '1234567890',
            'user_dob': '01/01/1990',
            'password': 'test',
            'repassword': 'test'
        }
        User.objects.create_user(username=context.get('username'), email=context.get('username'),
                                 password=context.get('password'))
        user = authenticate(username=context.get('username'), password=context.get('password'))
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_home'), context)
        self.assertEqual(response.status_code, 200)
