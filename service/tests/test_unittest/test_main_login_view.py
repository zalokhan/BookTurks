import mock

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from service.tests.create_user import create_user, prepare_client
from service.tests.constants_models import context
from service.tests.dropbox_tools import mock_dropbox


class MainLoginViewTest(TestCase):
    """
    Test case for the Login Modules
    """

    @mock.patch('dropbox.Dropbox', autospec=True)
    def setUp(self, mock_dbx):
        """
        Initialization for all tests
        :return:
        """
        mock_dropbox(self, mock_dbx)

    def test_register_view_with_no_input(self):
        """
        Testing the login view
        :return:
        """
        client = Client()
        response = client.post(reverse('service:login'), follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_register_view_with_valid_user(self):
        """
        Testing the login view
        :return:
        """
        create_user()
        client = Client()

        client = prepare_client(client)

        response = client.post(reverse('service:login'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/usersetup/", 302))
        redirect_chain.append(("/home/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_register_view_with_disabled_user(self):
        """
        Testing the login view
        :return:
        """
        user = create_user()
        user.is_active = False
        user.save()
        client = Client()
        response = client.post(reverse('service:login'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)
