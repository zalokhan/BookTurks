from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from service.tests.create_user import create_user, create_user_model_in_database, context


class UserHomeViewTest(TestCase):
    """
    Test case for the User Home Page
    """

    def test_user_valid(self):
        """
        Testing the dashboard view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        session = client.session
        session['user_profile_model'] = "mock_model"
        session.save()
        response = client.post(reverse('service:user_home'), context)
        self.assertEqual(response.status_code, 200)

    def test_user_not_authenticated(self):
        """
        Testing the dashboard view
        :return:
        """
        client = Client()
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_home'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/?next=/home/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)
