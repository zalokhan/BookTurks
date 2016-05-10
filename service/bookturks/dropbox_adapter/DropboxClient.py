from django.conf import settings
from service.bookturks.Constants import QUIZ_HOME


class DropboxClient:
    """
     DropBox client
        Quiz related functions
    """

    def __init__(self):
        """
        Create a DropBox Client object
        """
        self.client = settings.DROPBOX_CLIENT

    def upload_file(self, content, filename):
        """
        Uploads content creating a new file
        :param content: content of file
        :param filename: create a file with this name on dropbox
        :return: List of File objects of all quizzes matching the filter
        """

        return self.client.files_upload(content, filename)

    def list_quiz_files(self, filters=None):
        """
        Lists the quiz files filtering out required quiz results
        :param filters: filters to be provided in future
        :return: List of File objects of all quizzes matching the filter
        """

        list_of_files = self.client.files_list_folder(QUIZ_HOME)
        if not filters:
            while True:
                for i in list_of_files.entries:
                    print i.name
                if not list_of_files.has_more:
                    break
                else:
                    list_of_files = self.client.files_list_folder_continue(list_of_files.cursor)
