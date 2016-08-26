from django.test import TestCase, Client

from service.bookturks.adapters import QuizAdapter, UserAdapter
from service.tests.constants_models import context
from service.tests.create_user import create_user


class QuizAdapterTest(TestCase):
    """
    Test case for the Quiz Adapter
    """

    def setUp(self):
        """
        Initialization for all tests
        :return:
        """
        self.quiz_adapter = QuizAdapter()
        self.user_adapter = UserAdapter()

    def test_create_model(self):
        """
        Testing the create quiz model method
        :return: Asserts
        """
        client = Client()
        create_user()
        client.login(username=context.get('username'), password=context.get('password'))

        # Empty quiz_id and parameters should not create model
        self.assertRaises(ValueError, self.quiz_adapter.create_model, quiz_id=" ",
                          quiz_name=" ",
                          quiz_description=None,
                          quiz_owner=None)

        # Valid flow
        user = self.user_adapter.create_and_save_model(username=context.get('username'),
                                                       first_name=context.get('user_first_name'),
                                                       last_name=context.get('user_last_name'),
                                                       phone=context.get('user_phone'),
                                                       dob=context.get('user_dob'))

        self.assertEqual(self.quiz_adapter.exists(quiz_id="quiz_id"), None)
        quiz_model = self.quiz_adapter.create_and_save_model(quiz_id="quiz_id",
                                                             quiz_name="quiz_name",
                                                             quiz_description="quiz_description",
                                                             quiz_owner=user)
        self.assertEqual(self.quiz_adapter.exists("quiz_id"), quiz_model)

        # Duplicate quiz should not create model too
        self.assertRaises(ValueError, self.quiz_adapter.create_model,
                          quiz_id='quiz_id',
                          quiz_name="quiz_name",
                          quiz_description="quiz_description",
                          quiz_owner=user)
