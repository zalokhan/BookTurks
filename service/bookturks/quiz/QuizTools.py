import os
import json
import re
from service.bookturks.dropbox_adapter.DropboxClient import DropboxClient
from dropbox.exceptions import ApiError
from django.conf import settings


class QuizTools:
    """
    Creates quizzes
    Parses and checks for errors
    Add functions in future
    """

    def __init__(self):
        self.dbx = DropboxClient(settings.DROPBOX_CLIENT)
        pass

    def get_quiz_id(self, username, quiz_name):
        """
        Concatenate to form the quiz_id
        :param username:
        :param quiz_name:
        :return:
        """
        quiz_id = "_".join([username, quiz_name])
        if re.match("^[A-Za-z0-9_ -]*$", quiz_name):
            quiz_id = ''.join(character for character in quiz_id if character.isalnum())
            return quiz_id
        else:
            return None

    def create_filename(self, quiz):
        """
        Create filename for dropbox upload
        :param quiz:
        :return:
        """
        if not quiz or not quiz.quiz_owner or not str(quiz.quiz_owner).strip() or \
                not quiz.quiz_id or not str(quiz.quiz_id).strip():
            raise ValueError("QuizMaker:create_filename:Invalid Quiz model passed")
        return "".join(["/quiz/", str(quiz.quiz_id), ".JSON"])

    def create_content(self, quiz_form, quiz_data, quiz_model, answer_key):
        """
        Creates quiz content to be uploaded to storage
        :param quiz_form:
        :param quiz_data:
        :param quiz_model:
        :param answer_key:
        :return:
        """
        content = dict()

        # Converting from immutable dict to mutable
        answer_key = dict(answer_key)

        if 'csrfmiddlewaretoken' in answer_key:
            # Not required in the answer key so deleting
            del answer_key['csrfmiddlewaretoken']

        if not quiz_form or not quiz_data or not quiz_model or not answer_key:
            raise ValueError("QuizMaker:create_quiz_content:Parameter missing quiz, quiz_data, quiz_form or answer_key")
        if not quiz_model.quiz_id or not quiz_model.quiz_name:
            raise ValueError("QuizMaker:create_quiz_content:Invalid Quiz model passed")

        content['quiz_id'] = quiz_model.quiz_id
        content['quiz_name'] = quiz_model.quiz_name
        content['quiz_description'] = quiz_model.quiz_description
        content['quiz_owner'] = quiz_model.quiz_owner.username
        content['quiz_form'] = quiz_form
        content['quiz_data'] = quiz_data
        content['answer_key'] = answer_key
        try:
            content = json.dumps(content, ensure_ascii=False)
        except Exception, err:
            print (err)
            raise
        return content

    def parse_form(self, quiz_form):
        """
        Removes redundant data from form
        :param quiz_form: String form data
        :return: Modified form
        """
        form_tags = quiz_form.split('<')

        # Checking if less html tags then something is wrong or empty form has been submitted
        if len(form_tags) < 10:
            raise ValueError(
                "QuizMaker:quiz_form_data_parser:Empty quizzes cannot be submitted. Form_data cannot be empty.")

        # One more check to make sure that the form submitted has relevant tags.
        # Need to avoid script attacks
        if "rendered-form" in form_tags[1] and "form action=" in form_tags[2]:
            pass
        else:
            raise ValueError(
                "QuizMaker:quiz_form_data_parser:Quiz form is not properly generated. Something wrong with data")

        # Removing redundant lines
        # <div rendered-form></div>
        # <form></form>
        form_tags = form_tags[3:-4]
        final_form = "<" + "<".join(form_tags)
        return final_form

    def upload_quiz(self, content, filename):
        """
        Uploads file to storage
        :param content:
        :param filename:
        :return:
        """
        try:
            return_code = self.dbx.upload_file(content=content, filename=filename)
        except Exception, err:
            # TODO: Handle this properly
            print (err)
            return None
        return return_code

    def download_quiz_content(self, quiz_model):
        """
        Downloads the quiz and returns the content as JSON
        :param quiz_model:
        :return:
        """
        if not quiz_model or not quiz_model.quiz_id or not quiz_model.quiz_owner:
            raise ValueError("Invalid model is passed. Quiz not recognized.")
        path, metadata = self.dbx.get_file(filename=self.create_filename(quiz_model))
        quiz_file = open(path, 'r')
        content = ""
        while True:
            temp_data = quiz_file.read(100)
            if not temp_data:
                break
            content += temp_data
        quiz_file.close()
        os.remove(path)
        return json.loads(content)
