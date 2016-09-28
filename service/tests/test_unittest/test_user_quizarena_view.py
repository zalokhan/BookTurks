import uuid

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client

from service.bookturks.Constants import USER_PROFILE_MODEL
from service.bookturks.serializer import serialize
from service.tests.constants_models import context, mock_quiz_complete_model, mock_user_profile_model
from service.tests.create_user import create_user, prepare_client
from service.tests.test_setup_teardown.quiz_test_setup import QuizTest


class UserQuizArenaViewTest(QuizTest):
    """
    Test case for the Quiz Arena pages
    """

    def test_user_quizarena_view_without_login(self):
        """
        Testing the user quizarena view
        :return: Asserts
        """

        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)

        response = client.post(reverse('service:user_quizarena_home'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/?next=/quizarena/home/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quizarena_home_view_with_valid_inputs(self):
        """
        Testing the user quizarena view
        :return: Asserts
        """

        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing quiz model to be displayed
        self.quiz_adapter.create_and_save_model(quiz_name="mock_name",
                                                quiz_description="mock_description",
                                                quiz_owner=self.mock_user)

        response = client.post(reverse('service:user_quizarena_home'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quizarena_solve_view_with_valid_inputs(self):
        """
        Testing the user quizarena view
        :return: Asserts
        """

        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing quiz model to be displayed
        quiz = self.quiz_adapter.create_and_save_model(quiz_name="mock_name",
                                                       quiz_description="mock_description",
                                                       quiz_owner=self.mock_user)
        quiz_complete_model = mock_quiz_complete_model
        quiz_complete_model.quiz_model = quiz

        # Preparing session for attempts check while solving quizzes. Needs user_profile_model
        session = client.session
        session[USER_PROFILE_MODEL] = mock_user_profile_model
        session.save()

        # Preparing mock file for test
        with open("".join([settings.BASE_DIR, "/service/tmp", self.quiz_tools.create_filename(quiz)]),
                  'wb') as mock_file:
            mock_file.write(serialize(quiz_complete_model))
            mock_file.close()

        # Attempt the quiz (attempt = 1)
        response = client.post(reverse('service:user_quizarena_solve', kwargs={'quiz_id': quiz.quiz_id}), context,
                               follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quizarena_solve_view_with_invalid_quiz_id(self):
        """
        Testing the user quizarena view
        :return: Asserts
        """

        client = Client()
        create_user()
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_quizarena_solve', kwargs={'quiz_id': uuid.uuid4()}), context,
                               follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quizarena/home/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quizarena_result_view_with_invalid_inputs(self):
        """
        Testing the user quizarena view
        :return: Asserts
        """

        client = Client()
        create_user()
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_quizarena_result'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quizarena/home/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quizarena_result_view_with_valid_inputs(self):
        """
        Testing the user quizarena view
        :return: Asserts
        """
        client = Client()
        create_user()
        client = prepare_client(client)
        client.login(username=context.get('username'), password=context.get('password'))
        # Preparing quiz model to be displayed
        quiz = self.quiz_adapter.create_and_save_model(quiz_name="mock_name",
                                                       quiz_description="mock_description",
                                                       quiz_owner=self.mock_user)
        quiz_complete_model = mock_quiz_complete_model
        quiz_complete_model.quiz_model = quiz

        # Preparing session
        session = client.session
        session['quiz'] = quiz
        session.save()

        # Preparing mock file for test
        with open("".join([settings.BASE_DIR, "/service/tmp", self.quiz_tools.create_filename(quiz)]),
                  'wb') as mock_file:
            mock_file.write(serialize(quiz_complete_model))
            mock_file.close()

        response = client.post(reverse('service:user_quizarena_result'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        self.assertEqual(response.redirect_chain, redirect_chain)
