import dropbox
from django.conf import settings
from service.bookturks.Constants import QUIZ_HOME


class DropboxClient:
    """
     DropBox client
        Quiz related functions
    """

    def __init__(self, client):
        """
        Create a DropBox Client object
        """
        self.client = client

    def upload_file(self, content, filename):
        """
        Uploads content creating a new file
        :param content: content of file
        :param filename: create a file with this name on dropbox
        :return: file id from dropbox
        """
        # TODO: Upload file in chunks to avoid big upload
        return self.client.files_upload(content, filename, mode=dropbox.files.WriteMode.overwrite)

    def delete_file(self, filename):
        """
        Permanantly deletes the file from dropbox
        :param filename: Absolute filename with path
        :return:
        """
        return self.client.files_delete(filename)

    def get_file(self, filename):
        """
        Downloads file from storage and saves in the base root folder
        :param filename:
        :return:
        """
        download_path = "".join([settings.BASE_DIR, "/service/tmp", filename])
        return download_path, self.client.files_download_to_file(download_path=download_path, path=filename)

    """
    Quiz Specific functions for dropbox
    """

    def list_all_quiz_files(self, filters=None):
        """
        Lists the quiz files filtering out required quiz results
        :param filters: filters to be provided in future
        :return: List of File objects of all quizzes matching the filter
        """
        result_list = list()
        list_of_files = self.client.files_list_folder(QUIZ_HOME)
        if not filters:
            while True:
                for entry in list_of_files.entries:
                    result_list.append(entry)
                if not list_of_files.has_more:
                    break
                else:
                    list_of_files = self.client.files_list_folder_continue(list_of_files.cursor)
        return result_list

    def list_quiz_files_for_user(self, username):
        """
        For the input user, list all the quiz files owned
        :param username:
        :return:
        """
        result_list = list()
        list_of_files = self.client.files_search(path=QUIZ_HOME, query=username, start=0, )
        while True:
            for match in list_of_files.matches:
                result_list.append(match)
            if not list_of_files.more:
                break
            else:
                # Check if more than 100 files are available and search in batchse of 100.
                list_of_files = self.client.files_search(path=QUIZ_HOME, query=username, start=list_of_files.start)
        return result_list
