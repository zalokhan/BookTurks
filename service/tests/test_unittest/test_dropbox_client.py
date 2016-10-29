import os

from django.conf import settings
from django.test import TestCase

from service.bookturks.Constants import QUIZ_HOME
from service.bookturks.dropbox_adapter.DropboxClient import DropboxClient
from service.bookturks.serializer import serialize, deserialize


class DropboxClientTest(TestCase):
    """
    Test case for the DropBox Client
    """

    def setUp(self):
        """
        Initialization for all tests
        :return:
        """
        self.dbx = DropboxClient(settings.DROPBOX_CLIENT)

    def test_dropbox_upload_find_remove_file(self):
        """
        Testing the dropbox client
        :return:
        """
        mock_filename = "".join([QUIZ_HOME, "/mock_user_quiz_name"])

        # Checking uploads
        upload_result = self.dbx.upload_file(content=serialize("mock_content"), filename=mock_filename)
        self.assertIsNotNone(upload_result)
        self.assertEqual(mock_filename, upload_result.path_display)

        # Checking different queries
        all_quiz_list = self.dbx.list_all_quiz_files()
        self.assertGreaterEqual(len(all_quiz_list), 1)
        quiz_for_mock_user = self.dbx.list_quiz_files_for_user("mock_user")
        self.assertEqual(quiz_for_mock_user[0].metadata.path_display, mock_filename)

        # Checking downloads
        path, download_result = self.dbx.get_file(mock_filename)
        with open(path, 'rb') as quiz_file:
            content = quiz_file.read()
            quiz_file.close()
        os.remove(path)
        self.assertEqual(deserialize(content), "mock_content")

        # Checking deletions
        delete_result = self.dbx.delete_file(mock_filename)
        self.assertEqual(mock_filename, delete_result.path_display)
        quiz_for_mock_user = self.dbx.list_quiz_files_for_user("mock_user")
        self.assertIs(len(quiz_for_mock_user), 0)
