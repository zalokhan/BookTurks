import os
import re

from django.conf import settings
from dropbox.exceptions import ApiError

from service.bookturks.Constants import USER_PROFILE_MODEL
from service.bookturks.adapters.QuizTagAdapter import QuizTagAdapter
from service.bookturks.dropbox_adapter.DropboxClient import DropboxClient
from service.bookturks.models.QuizResultModel import QuizResultModel
from service.bookturks.serializer import deserialize
from service.bookturks.serializer import serialize


class QuizTools(object):
    """
    Creates quizzes
    Parses and checks for errors
    Add functions in future
    """

    def __init__(self):
        self.dbx = DropboxClient(settings.DROPBOX_CLIENT)

    @staticmethod
    def get_quiz_id(username, quiz_name):
        """
        Concatenate to form the quiz_id
        :param username:
        :param quiz_name:
        :return:
        """
        if not quiz_name.rstrip():
            raise ValueError("Quiz Name cannot be blank")
        quiz_id = "_".join([username, quiz_name.lower()])
        if re.match("^[A-Za-z0-9_ -]*$", quiz_name):
            quiz_id = ''.join(character for character in quiz_id if character.isalnum())
            if quiz_id.rstrip():
                return quiz_id
        else:
            raise ValueError("The quiz Name can contain ony alphanumeric characters, spaces, '-', '?' and '_'")

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

    @staticmethod
    def parse_form(quiz_form):
        """
        Removes redundant data from form
        :param quiz_form: String form data
        :return: Modified form
        """
        form_tags = quiz_form.split('<')

        # Checking if less html tags then something is wrong or empty form has been submitted
        if len(form_tags) < 10:
            raise ValueError(
                "Empty quizzes cannot be submitted. Form cannot be empty.")

        # One more check to make sure that the form submitted has relevant tags.
        # Need to avoid script attacks
        if "rendered-form" in form_tags[1] and "form action=" in form_tags[2]:
            pass
        else:
            raise ValueError(
                "Quiz form is not properly generated. Something wrong with data")

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
            path, metadata = self.dbx.get_file(filename=QuizTools.create_filename(quiz_model))
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
            QuizTools.content_verifier(deserialized_content)
        except ValueError as err:
            # TODO: Delete this quiz from dropbox and remove it from the database as it is now useless.
            # print (err)
            return None
        return deserialized_content

    @staticmethod
    def compare_quiz_dict(answer_key, user_answer_key):
        """
        Compares the 2 dictionaries. Only works with quiz dicts
        :param answer_key:
        :param user_answer_key:
        :return: right answers, wrong answers
        """
        correct_answers = list()
        wrong_answers = list()
        for key in answer_key.keys():
            l_ak = answer_key.get(key)
            l_uak = user_answer_key.get(key)
            if not l_uak:
                wrong_answers.append(key)
            elif l_ak != l_uak:
                wrong_answers.append(key)
            else:
                correct_answers.append(key)
        return correct_answers, wrong_answers

    @staticmethod
    def get_quiz_result(quiz_model, answer_key, user_answer_key):
        """
        Checks and returns the result of the quiz
        :param quiz_model:
        :param answer_key:
        :param user_answer_key:
        :return:
        """
        if 'csrfmiddlewaretoken' in user_answer_key:
            del user_answer_key['csrfmiddlewaretoken']
        if 'csrfmiddlewaretoken' in answer_key:
            del answer_key['csrfmiddlewaretoken']
        max_score = len(answer_key.keys())

        # Compares the answer key and the solution.
        correct_answers, wrong_answers = QuizTools.compare_quiz_dict(answer_key, user_answer_key)
        result = QuizResultModel(quiz_model=quiz_model,
                                 answer_key=answer_key,
                                 user_answer_key=user_answer_key,
                                 correct_answers=correct_answers,
                                 wrong_answers=wrong_answers,
                                 correct_score=len(correct_answers),
                                 wrong_score=max_score - len(correct_answers),
                                 max_score=max_score)
        return result

    def delete_quiz_from_storage(self, quiz):
        """
        Completely deletes quiz from storage only
        :param quiz:
        :return:
        """

        if not quiz or not quiz.quiz_id or not quiz.quiz_owner:
            raise ValueError("Quiz model invalid")

        filename = QuizTools.create_filename(quiz)
        try:
            self.dbx.delete_file(filename)
        except ApiError:
            raise ValueError("Quiz file not found in storage.")

    @staticmethod
    def unlink_all_tags_of_quiz(quiz):
        """
        Unlinks all the tags of the quiz
        :param quiz:
        :return:
        """
        for tag in quiz.quiztag_set.all():
            QuizTagAdapter.unlink_quiz(tag_name=tag.tag_name, quiz_id=quiz.quiz_id)

    @staticmethod
    def check_attempt_eligibility(user_profile_model, quiz_complete_model, quiz_id):
        """
        Checks if the user still has number of attempts left for this quiz
        :return:
        """
        attempted = 0
        for quiz_result in user_profile_model.attempted_quiz:
            if quiz_result.quiz_model.quiz_id == quiz_id:
                attempted = quiz_result.attempts
                break
        if attempted >= int(quiz_complete_model.attempts):
            raise ValueError("Attempts exceeded.")