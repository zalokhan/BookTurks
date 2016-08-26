from django.test import TestCase, Client

from service.bookturks.adapters import UserAdapter
from service.tests.constants_models import context
from service.tests.create_user import create_user


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
        self.assertRaises(ValueError, self.user_adapter.create_model, username=" ")

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
        self.assertRaises(ValueError, self.user_adapter.create_model, username=context.get('username'))
