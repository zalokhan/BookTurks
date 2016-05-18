from django.test import TestCase

import mock
from service.bookturks.dropbox_adapter.DropboxClient import DropboxClient
from service.bookturks.Constants import QUIZ_HOME


class MockFileList:
    entries = ["mock_file_1", "mock_file_2", "mock_file_3"]
    has_more = False

    def __init__(self):
        return

    def __call__(self, *args, **kwargs):
        return self


class DropboxClientTest(TestCase):
    """
    Test case for the DropBox Client
    """

    @mock.patch('dropbox.Dropbox', autospec=True)
    def setUp(self, mock_dbx):
        """
        Initialization for all tests
        :return:
        """
        dbx = mock_dbx.return_value
        dbx.files_upload.return_value = "mock_id"
        self.mock_file_list = MockFileList()
        dbx.files_list_folder.return_value = self.mock_file_list
        self.dbx = dbx
        self.client = DropboxClient(dbx)

    def test_dropbox_upload_file(self):
        """
        Testing the dropbox client
        :return:
        """
        result = self.client.upload_file(content="mock_content", filename="mock_filename")
        self.assertEqual("mock_id", result)
        self.dbx.files_upload.assert_called_once_with("mock_content", "mock_filename")

    def test_dropbox_list_quiz_files(self):
        """
        Testing dropbox client
        :return:
        """
        result = self.client.list_quiz_files()
        self.assertEqual(self.mock_file_list.entries, result)
        self.dbx.files_list_folder.assert_called_once_with(QUIZ_HOME)
