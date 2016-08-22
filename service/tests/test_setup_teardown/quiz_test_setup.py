import mock
from django.test import TestCase

from service.bookturks.adapters.QuizAdapter import QuizAdapter
from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.quiz.QuizTools import QuizTools
from service.tests.dropbox_tools import mock_dropbox, restore_dropbox


class QuizTest(TestCase):
    """
    Parent class for quiz test cases.
    Do not create Clients here because every test case has its own requirement.
    Some tests might login the client and some will not.
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

    def tearDown(self):
        restore_dropbox()
