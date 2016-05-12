"""
Creates quizzes
Parses and checks for errors
Uploads the file to DropBox with relevant naming conventions for faster searches.
Add functions in future
"""
from service.dropbox_adapter.DropboxClient import DropboxClient


def create_quiz(content, quiz_name):
    """
    Create quiz with dict contents
    :param content: Dictionary containing entire quiz
    :return: Dropbox file metadata
    """
    dbx = DropboxClient()
    return_code = dbx.upload_file(content=content, filename="/quiz/"+quiz_name)
    return return_code
