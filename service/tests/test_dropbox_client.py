from django.test import TestCase

import mock
import dropbox
from service.bookturks.dropbox_adapter.DropboxClient import DropboxClient
from service.bookturks.Constants import QUIZ_HOME
from service.tests.dropbox_tools import MockFileList, MOCK_FILE_CONTENT


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
        dbx.files_delete.return_value = None
        # It should return an object not contents
        dbx.files_download_to_file.return_value = MOCK_FILE_CONTENT
        self.dbx = dbx
        self.client = DropboxClient(dbx)

    def test_dropbox_upload_file(self):
        """
        Testing the dropbox client
        :return:
        """
        result = self.client.upload_file(content="mock_content", filename="mock_filename")
        self.assertEqual("mock_id", result)
        self.dbx.files_upload.assert_called_once_with("mock_content", "mock_filename",
                                                      mode=dropbox.files.WriteMode.overwrite)

    def test_dropbox_list_all_quiz_files(self):
        """
        Testing dropbox client
        :return:
        """
        result = self.client.list_all_quiz_files()
        self.assertEqual(self.mock_file_list.entries, result)
        self.dbx.files_list_folder.assert_called_once_with(QUIZ_HOME)
