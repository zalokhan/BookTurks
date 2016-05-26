from django.test import TestCase, Client

from service.tests.create_user import create_user, context
from service.bookturks.adapters.UserAdapter import UserAdapter


class UserAdapterTest(TestCase):
    """
    Test case for the User Adapter
    """

    def setUp(self):
        """
        Initialization for all tests
        :return:
        """
        self.user_adapter = UserAdapter()

    def test_create_model(self):
        """
        Testing the create user method
        :return: Asserts
        """
        client = Client()
        create_user()
        client.login(username=context.get('username'), password=context.get('password'))

        # Empty username should not create model
        user = self.user_adapter.create_model(username=" ")
        self.assertEqual(user, None)

        # Valid flow
        user = self.user_adapter.create_model(username=context.get('username'),
                                              first_name=context.get('user_first_name'),
                                              last_name=context.get('user_last_name'),
                                              phone=context.get('user_phone'),
                                              dob=context.get('user_dob'))
        self.assertEqual(self.user_adapter.exists(user), None)
        user.save()
        self.assertEqual(self.user_adapter.exists(context.get('username')), user)

        # Duplicate user should not create model too
        user = self.user_adapter.create_model(username=context.get('username'))
        self.assertEqual(user, None)
