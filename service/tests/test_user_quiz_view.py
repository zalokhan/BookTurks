from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from service.tests.create_user import create_user, context


class UserQuizViewTest(TestCase):
    """
    Test case for the Quiz pages
    """

    def test_user_quiz_init_view(self):
        """
        Testing the user quiz view
        :return: Asserts
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_quiz_init'), context)
        self.assertEqual(response.status_code, 200)

    def test_user_quiz_maker_view_with_valid_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        quiz_parameters = dict(context)

        quiz_parameters['quiz_id'] = 'test_quiz_id'
        quiz_parameters['quiz_name'] = 'test_quiz_name'
        quiz_parameters['quiz_description'] = 'test_quiz_description'

        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_quiz_maker'), quiz_parameters)
        self.assertEqual(response.status_code, 200)

    def test_user_quiz_verifier_view_with_valid_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        quiz_parameters = dict(context)

        quiz_parameters['quiz_id'] = 'test_quiz_id'
        quiz_parameters['quiz_name'] = 'test_quiz_name'
        quiz_parameters['quiz_description'] = 'test_quiz_description'

        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_quiz_maker'), quiz_parameters)
        self.assertEqual(response.status_code, 200)
