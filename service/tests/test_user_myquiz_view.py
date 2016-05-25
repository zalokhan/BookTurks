from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User as AuthUser
import mock
import json

from service.tests.create_user import create_user, context
from service.bookturks.adapters.QuizAdapter import QuizAdapter
from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.quiz.QuizTools import QuizTools
from service.tests.dropbox_tools import MockFileList, MOCK_FILE_CONTENT


class UserMyquizViewTest(TestCase):
    """
    Test case for the MyQuiz pages
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

        dbx = mock_dbx.return_value
        dbx.files_upload.return_value = "mock_id"
        self.mock_file_list = MockFileList()
        dbx.files_list_folder.return_value = self.mock_file_list
        dbx.files_delete.return_value = None
        # It should return an object not contents
        dbx.files_download_to_file.return_value = MOCK_FILE_CONTENT
        self.dbx = dbx
        # Creating test user in database
        new_user = self.user_adapter.create_and_save_model(
            username='test@email.com',
            first_name='testfirstname',
            last_name='testlastname',
            phone='1234567890',
            dob='01/01/1990',
        )
        self.mock_user = new_user
        settings.DROPBOX_CLIENT = self.dbx

    def test_user_myquiz_view_without_login(self):
        """
        Testing the user myquiz view
        :return: Asserts
        """

        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)

        response = client.post(reverse('service:user_myquiz_home'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/?next=/myquiz/home/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_myquiz_home_view_with_valid_inputs_with_no_quiz(self):
        """
        Testing the user myquiz view
        :return: Asserts
        """

        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        response = client.post(reverse('service:user_myquiz_home'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_myquiz_home_view_with_valid_inputs_with_one_quiz(self):
        """
        Testing the user myquiz view
        :return: Asserts
        """

        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        # Preparing quiz model to be displayed
        self.quiz_adapter.create_and_save_model(quiz_id="test_id",
                                                quiz_name="mock_name",
                                                quiz_description="mock_description",
                                                quiz_owner=self.mock_user)

        response = client.post(reverse('service:user_myquiz_home'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_myquiz_info_view_with_valid_inputs(self):
        """
        Testing the user myquiz info page
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        # Preparing quiz model to be displayed
        quiz = self.quiz_adapter.create_and_save_model(quiz_id="test_id",
                                                       quiz_name="mock_name",
                                                       quiz_description="mock_description",
                                                       quiz_owner=self.mock_user)
        # Preparing mock file for test
        mock_file = open("".join([settings.BASE_DIR, "/service/tmp", self.quiz_tools.create_filename(quiz)]), 'w')
        mock_file.write(json.dumps(MOCK_FILE_CONTENT))
        mock_file.close()

        response = client.post(reverse('service:user_myquiz_info', kwargs={'quiz_id': 'test_id'}), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_myquiz_info_view_with_invalid_inputs(self):
        """
        Testing the user myquiz info page
        :return:
        """
        client = Client()
        create_user()

        # Creating attacker account which tries to delete other persons quizzes
        AuthUser.objects.create_user(username="mock2@mock.com", email=context.get('mock2@mock.com'),
                                     password=context.get('password'))
        client.login(username="mock2@mock.com", password=context.get('password'))

        # Quiz not yet created
        response = client.post(reverse('service:user_myquiz_info', kwargs={'quiz_id': 'test_id'}), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/home/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

        # Preparing quiz model to be displayed
        quiz = self.quiz_adapter.create_and_save_model(quiz_id="test_id",
                                                       quiz_name="mock_name",
                                                       quiz_description="mock_description",
                                                       quiz_owner=self.mock_user)
        # Preparing mock file for test
        mock_file = open("".join([settings.BASE_DIR, "/service/tmp", self.quiz_tools.create_filename(quiz)]), 'w')
        mock_file.write(json.dumps(MOCK_FILE_CONTENT))
        mock_file.close()

        # User not allowed to modify this
        response = client.post(reverse('service:user_myquiz_info', kwargs={'quiz_id': 'test_id'}), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/home/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)
