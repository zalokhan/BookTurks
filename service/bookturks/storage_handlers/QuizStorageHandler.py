import os

from django.conf import settings
from dropbox.exceptions import ApiError

from service.bookturks.dropbox_adapter.DropboxClient import DropboxClient
from service.bookturks.serializer import serialize, deserialize


class QuizStorageHandler(object):
    """
    Quiz Storage Handler
    """

    def __init__(self):
        self.dbx = DropboxClient(settings.DROPBOX_CLIENT)

    @staticmethod
    def create_filename(quiz):
        """
        Create filename for dropbox upload
        :param quiz:
        :return:
        """
        if not quiz or not quiz.quiz_owner or not str(quiz.quiz_owner).strip() or \
                not quiz.quiz_id or not str(quiz.quiz_id).strip():
            raise ValueError("QuizMaker:create_filename:Invalid Quiz model passed")
        return "".join(["/quiz/", str(quiz.quiz_id)])

    @staticmethod
    def create_content(quiz_complete_model, answer_key):
        """
        Creates quiz content to be uploaded to storage
        :param quiz_complete_model:
        :param answer_key:
        :return:
        """

        if not answer_key:
            raise ValueError("QuizTools :: Invalid argument passed.")

        # Converting from immutable dict to mutable
        answer_key = dict(answer_key)

        if 'csrfmiddlewaretoken' in answer_key:
            # Not required in the answer key so deleting
            del answer_key['csrfmiddlewaretoken']

        if not quiz_complete_model or not answer_key:
            raise ValueError("Quiz content or answer key cannot be empty.")
        if not quiz_complete_model.quiz_model.quiz_id or not quiz_complete_model.quiz_model.quiz_name:
            raise ValueError("QuizMaker:create_quiz_content:Invalid Quiz model")

        quiz_complete_model.answer_key = answer_key

        try:
            content = serialize(quiz_complete_model)
        except Exception:
            raise
        return content

    def upload_quiz(self, content, filename):
        """
        Uploads file to storage
        :param content:
        :param filename:
        :return:
        """
        try:
            return_code = self.dbx.upload_file(content=content, filename=filename)
        except Exception:
            # TODO: Handle this properly
            raise
        return return_code

    @staticmethod
    def content_verifier(content):
        """
        Verifies the content
        :param content:
        :return:
        """
        if not content:
            raise ValueError("Invalid quiz_file stored")

    def download_quiz_content(self, quiz_model):
        """
        Downloads the quiz and returns the content as JSON
        :param quiz_model:
        :return:
        """
        if not quiz_model or not quiz_model.quiz_id or not quiz_model.quiz_owner:
            raise ValueError("Invalid model is passed. Quiz not recognized.")
        try:
            path, metadata = self.dbx.get_file(filename=QuizStorageHandler.create_filename(quiz_model))
        except ApiError as err:
            # TODO: Something went wrong here. Handle this properly
            # print err
            return None
        # Open files with the keyword 'with' only
        with open(path, 'rb') as quiz_file:
            content = quiz_file.read()
            deserialized_content = deserialize(content)
            quiz_file.close()
        os.remove(path)

        try:
            QuizStorageHandler.content_verifier(deserialized_content)
        except ValueError as err:
            # TODO: Delete this quiz from dropbox and remove it from the database as it is now useless.
            # print (err)
            return None
        return deserialized_content

    def delete_quiz_from_storage(self, quiz):
        """
        Completely deletes quiz from storage only
        :param quiz:
        :return:
        """

        if not quiz or not quiz.quiz_id or not quiz.quiz_owner:
            raise ValueError("Quiz model invalid")

        filename = QuizStorageHandler.create_filename(quiz)
        try:
            self.dbx.delete_file(filename)
        except ApiError:
            raise ValueError("Quiz file not found in storage.")
