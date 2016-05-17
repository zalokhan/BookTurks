from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from service.models import User


class RegisterViewTest(TestCase):
    """
    Test case for the Register Page
    """

    def test_register_view(self):
        """
        Testing the register view
        :return:
        """
        client = Client()
        response = client.get(reverse('service:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_check_with_valid_inputs(self):
        """
        Checking the post method and all valid inputs
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
        response = client.post(reverse('service:register_check'), context)
        self.assertEqual(response.status_code, 302)

        # Test if user is created in models
        try:
            get_object_or_404(User, username=context.get('username'))
        except Http404:
            raise Http404

        user = authenticate(username=context.get('username'), password=context.get('password'))
        self.assertEqual(user.is_active, True)
