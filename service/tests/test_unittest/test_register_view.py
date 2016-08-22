from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from service.tests.create_user import create_user
from service.tests.constants_models import context

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
        response = client.post(reverse('service:register_check'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

        # Test if user is created in models
        try:
            get_object_or_404(User, username=context.get('username'))
        except Http404:
            raise Http404

        user = authenticate(username=context.get('username'), password=context.get('password'))
        self.assertEqual(user.is_active, True)

    def test_register_check_with_wrong_password_confirmation(self):
        """
        Checking register check
        :return:
        """
        client = Client()
        params = dict(context)
        params['password'] = 'test'
        params['repassword'] = 'retest'
        response = client.post(reverse('service:register_check'), params, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/register/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

        # Test if exception raised
        with self.assertRaisesMessage(Http404, ''):
            get_object_or_404(User, username=params.get('username'))

        user = authenticate(username=params.get('username'), password=params.get('password'))
        self.assertEqual(user, None)

    def test_register_check_with_duplicate_id(self):
        """
        Checking register check
        :return:
        """
        client = Client()
        create_user()
        user = User(username=context.get('username'),
                    user_first_name=context.get('user_first_name'),
                    user_last_name=context.get('user_last_name'),
                    user_phone=context.get('user_phone'),
                    user_dob=context.get('user_dob'))
        user.save()

        response = client.post(reverse('service:register_check'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/register/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

        # Test if user is created in models
        try:
            get_object_or_404(User, username=context.get('username'))
        except Http404:
            raise Http404

        user.delete()
        user = authenticate(username=context.get('username'), password=context.get('password'))
        self.assertEqual(user.is_active, True)

    def test_register_check_with_wrong_username_format(self):
        """
        Checking register check
        :return:
        """
        client = Client()
        params = dict(context)
        params['username'] = 'test'
        response = client.post(reverse('service:register_check'), params, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/register/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

        # Test if exception raised
        with self.assertRaisesMessage(Http404, ''):
            get_object_or_404(User, username=params.get('username'))

        user = authenticate(username=params.get('username'), password=params.get('password'))
        self.assertEqual(user, None)

    def test_register_check_with_missing_inputs(self):
        """
        Checking register check
        :return:
        """
        client = Client()

        params = dict(context)
        del params['username']
        response = client.post(reverse('service:register_check'), params, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/register/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

        params = dict(context)
        del params['user_first_name']
        response = client.post(reverse('service:register_check'), params, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/register/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)
        user = authenticate(username=params.get('username'), password=params.get('password'))
        self.assertEqual(user, None)

        params = dict(context)
        del params['user_last_name']
        response = client.post(reverse('service:register_check'), params, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/register/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)
        user = authenticate(username=params.get('username'), password=params.get('password'))
        self.assertEqual(user, None)

        params = dict(context)
        del params['user_phone']
        response = client.post(reverse('service:register_check'), params, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/register/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)
        user = authenticate(username=params.get('username'), password=params.get('password'))
        self.assertEqual(user, None)

        params = dict(context)
        del params['user_dob']
        response = client.post(reverse('service:register_check'), params, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/register/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)
        user = authenticate(username=params.get('username'), password=params.get('password'))
        self.assertEqual(user, None)

        params = dict(context)
        del params['password']
        response = client.post(reverse('service:register_check'), params, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/register/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)
        user = authenticate(username=params.get('username'), password=params.get('password'))
        self.assertEqual(user, None)

        params = dict(context)
        del params['repassword']
        response = client.post(reverse('service:register_check'), params, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/register/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)
        user = authenticate(username=params.get('username'), password=params.get('password'))
        self.assertEqual(user, None)
