from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import mock

from django.contrib.auth.models import User as AuthUser
from service.tests.create_user import create_user, context, prepare_client
from service.bookturks.adapters.QuizAdapter import QuizAdapter
from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.quiz.QuizTools import QuizTools
from service.models import Quiz, User
from service.tests.dropbox_tools import mock_dropbox


class UserQuizCreateViewTest(TestCase):
    """
    Test case for the Quiz pages
    """

    @mock.patch('dropbox.Dropbox', autospec=True)
    def setUp(self, mock_dbx):
        """
        Initialization for all tests
        :return:
        """
        self.user_adapter = UserAdapter()
        self.quiz_adapter = QuizAdapter()
        self.quiz_tools = QuizTools()
        mock_dropbox(self, mock_dbx)
        # Creating test user in database
        new_user = self.user_adapter.create_and_save_model(
            username='test@email.com',
            first_name='testfirstname',
            last_name='testlastname',
            phone='1234567890',
            dob='01/01/1990',
        )
        self.mock_user = new_user

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
        response = client.post(reverse('service:user_quiz_maker'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_quiz_maker_view_with_empty_name(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        quiz_parameters = dict(context)

        quiz_parameters['quiz_name'] = ' '
        quiz_parameters['quiz_description'] = 'test_quiz_description'

        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_quiz_maker'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)

        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_maker_view_with_duplicate_name(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        quiz_parameters = dict(context)

        quiz_parameters['quiz_name'] = 'test_quiz_name'
        quiz_parameters['quiz_description'] = 'test_quiz_description'
        quiz = self.quiz_adapter.create_and_save_model(
            quiz_id=self.quiz_tools.get_quiz_id(user.username, quiz_parameters['quiz_name']),
            quiz_name="mock_name",
            quiz_description="mock_description",
            quiz_owner=self.mock_user)
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_quiz_maker'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)

        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)
        quiz.delete()

    def test_user_quiz_verifier_view_with_null_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_verifier_view_with_both_invalid_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['quiz_data'] = 'garbage'
        quiz_parameters['quiz_form'] = 'garbage'
        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_verifier_view_with_form_invalid_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['quiz_data'] = '<form-template>\r\n\t<fields>\r\n\t\t<field class="header" label="Header" ' \
                                       'type="header" subtype="h1"></field>\r\n\t</fields>\r\n</form-template>'
        quiz_parameters['quiz_form'] = "garbage"
        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_verifier_view_with_logically_invalid_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['quiz_data'] = '<form-template>\r\n\t<fields>\r\n\t\t<field class="header" label="Header" ' \
                                       'type="header" subtype="h1"></field>\r\n\t</fields>\r\n</form-template>'
        # <from > instead of <form>
        quiz_parameters['quiz_form'] = '<div id="rendered-form" style="padding-top: 40px; display: block;">\r\n    ' \
                                       '<from action="#"><div class=""><h1>Header</h1></div></form>\r\n    ' \
                                       '<button class="btn btn-default edit-form">Edit</button>\r\n</div>'
        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_verifier_view_with_less_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['quiz_data'] = '<form-template>\r\n\t<fields>\r\n\t\t<field class="header" label="Header" ' \
                                       'type="header" subtype="h1"></field>\r\n\t</fields>\r\n</form-template>'
        # <from > instead of <form>
        quiz_parameters['quiz_form'] = '<div id="rendered-form" style="padding-top: 40px; display: block;">\r\n    ' \
                                       '<form action="#"><div class=""></div></form>\r\n    ' \
                                       '<button class="btn btn-default edit-form">Edit</button>\r\n</div>'
        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_verifier_view_with_valid_inputs(self):
        """
        Testing the user maker quiz view with valid inputs
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['quiz_data'] = '<form-template>\r\n\t<fields>\r\n\t\t<field class="header" label="Header" ' \
                                       'type="header" subtype="h1"></field>\r\n\t</fields>\r\n</form-template>'
        quiz_parameters['quiz_form'] = '<div id="rendered-form" style="padding-top: 40px; display: block;">\r\n    ' \
                                       '<form action="#"><div class=""><h1>Header</h1></div></form>\r\n    ' \
                                       '<button class="btn btn-default edit-form">Edit</button>\r\n</div>'
        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_create_view_with_valid_inputs(self):
        """
        Testing create view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['answer_key'] = {'answer_key': 'test'}
        # Preparing session
        quiz = Quiz(
            quiz_id="test_id",
            quiz_name="mock_name",
            quiz_description="mock_description",
            quiz_owner=self.mock_user
        )
        client = prepare_client(client)
        session = client.session
        session['quiz_form'] = "mock_quiz_form"
        session['quiz_data'] = "mock_quiz_data"
        session['quiz'] = quiz
        session.save()
        # Testing response status code
        response = client.post(reverse('service:user_quiz_create'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/home/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_create_view_with_all_invalid_inputs(self):
        """
        Testing create view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['answer_key'] = {'answer_key': 'test'}
        # Testing response status code
        response = client.post(reverse('service:user_quiz_create'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_create_view_with_invalid_error_inputs(self):
        """
        Testing create view
        Handling exception
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['answer_key'] = 'answer_key'
        quiz_parameters['csrfmiddlewaretoken'] = 'test'

        # Preparing session
        quiz = Quiz(
            quiz_id="test_id",
            quiz_name="mock_name",
            quiz_description="mock_description",
            quiz_owner=self.mock_user
        )
        session = client.session
        session['quiz_data'] = "mock_quiz_data"
        session['quiz'] = quiz
        session.save()
        # Testing response status code
        response = client.post(reverse('service:user_quiz_create'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

        # Preparing session
        quiz = Quiz(
            quiz_name="mock_name",
            quiz_description="mock_description",
            quiz_owner=self.mock_user
        )
        session['quiz_form'] = "mock_quiz_form"
        session['quiz'] = quiz
        session.save()
        # Testing response status code
        response = client.post(reverse('service:user_quiz_create'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

        # Preparing session
        quiz = Quiz(
            quiz_id="test_id",
            quiz_description="mock_description",
            quiz_owner=self.mock_user
        )
        session['quiz'] = quiz
        session.save()
        # Testing response status code
        response = client.post(reverse('service:user_quiz_create'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_delete_with_all_valid_inputs(self):
        """
        Testing quiz delete view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        client = prepare_client(client)
        # Preparing quiz model to be deleted
        quiz = self.quiz_adapter.create_and_save_model(quiz_id="test_id",
                                                       quiz_name="mock_name",
                                                       quiz_description="mock_description",
                                                       quiz_owner=self.mock_user)
        quiz_parameters = dict(context)
        quiz_parameters['quiz_id'] = quiz.quiz_id

        # Assert quiz present
        self.assertEqual(self.quiz_adapter.exists(quiz.quiz_id), quiz)

        # Testing response status code
        response = client.post(reverse('service:user_quiz_delete'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/myquiz/home/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

        # Assert quiz deleted
        self.assertEqual(self.quiz_adapter.exists(quiz.quiz_id), None)

    def test_user_quiz_delete_with_invalid_user(self):
        """
        Testing quiz delete view
        :return:
        """
        client = Client()
        create_user()

        # Creating attacker account which tries to delete other persons quizzes
        AuthUser.objects.create_user(username="mock2@mock.com", email=context.get('mock2@mock.com'),
                                     password=context.get('password'))
        client.login(username="mock2@mock.com", password=context.get('password'))

        # Preparing quiz model to be deleted
        quiz = self.quiz_adapter.create_and_save_model(quiz_id="test_id",
                                                       quiz_name="mock_name",
                                                       quiz_description="mock_description",
                                                       quiz_owner=self.mock_user)
        quiz_parameters = dict(context)
        quiz_parameters['quiz_id'] = quiz.quiz_id

        # Assert quiz present
        self.assertEqual(self.quiz_adapter.exists(quiz.quiz_id), quiz)

        # Testing response status code
        response = client.post(reverse('service:user_quiz_delete'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/myquiz/home/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

        # Assert quiz present
        self.assertEqual(self.quiz_adapter.exists(quiz.quiz_id), quiz)
