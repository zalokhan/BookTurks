"""
Creates quizzes
Parses and checks for errors
Uploads the file to DropBox with relevant naming conventions for faster searches.
Add functions in future
"""
import json
from service.bookturks.dropbox_adapter.DropboxClient import DropboxClient
from django.conf import settings


def create_filename(owner, quizid):
    """
    Create filename for dropbox upload
    :param owner:
    :param quizid:
    :return:
    """
    return "/quiz/" + str(owner) + "_" + str(quizid) + ".JSON"


def create_quiz_content(quiz_form, quiz_data, quiz, answer_key):
    """
    Create quiz with dict contents
    :param quiz_form: HTML Form data
    :param quiz_data: Raw data without rendering from form builder
    :param quiz: quiz model
    :param answer_key: answer key in dictionary
    :return:
    """

    content = dict()

    # Converting from immutable dict to mutable
    answer_key = dict(answer_key)
    if 'csrfmiddlewaretoken' in answer_key:
        # Not required in the answer key so deleting
        del answer_key['csrfmiddlewaretoken']

    if not quiz_form or not quiz_data or not quiz or not answer_key:
        raise ValueError("QuizMaker:create_quiz_content:Parameter missing quiz, quiz_data, quiz_form or answer_key")
    if not quiz.quiz_id or not quiz.quiz_name:
        raise ValueError("QuizMaker:create_quiz_content:Invalid Quiz model passed")

    content['quiz_form'] = quiz_form
    content['quiz_data'] = quiz_data
    content['answer_key'] = json.dumps(answer_key, ensure_ascii=False)
    content = json.dumps(content, ensure_ascii=False)

    filename = create_filename(quiz.quiz_owner, quiz.quiz_id)

    try:
        dbx = DropboxClient(settings.DROPBOX_CLIENT)
        return_code = dbx.upload_file(content=content, filename=filename)
    except:
        return None
    return return_code


def quiz_form_data_parser(form_data):
    """
    Removes redundant data from form and adds csrf token and required padding
    :param form_data: String form data
    :return: Modified form
    """
    form_tags = form_data.split('<')

    if len(form_tags) < 10:
        raise ValueError(
            "QuizMaker:quiz_form_data_parser:Empty quizzes cannot be submitted. Form_data cannot be empty.")

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
