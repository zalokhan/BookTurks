from django.shortcuts import get_object_or_404
from django.http import Http404
from service.models import Quiz


def quiz_exists(quiz_id):
    """
    Check if quiz exists
    :param quiz_id:
    :return: True if exists else False
    """
    try:
        quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
        return quiz
    except Http404:
        return None


def create_new_quiz(quiz_id, quiz_name, quiz_description):
    """
    Creates new quiz
    :param quiz_id:
    :param quiz_name:
    :param quiz_description:
    :return:
    """
    if not quiz_id or not quiz_id.strip() or \
            not quiz_name or not quiz_name.strip() or \
            not quiz_description or not quiz_description.strip():
        return False
    try:
        get_object_or_404(Quiz, quiz_id=quiz_id)
    except Http404:
        quiz = Quiz(quiz_id=quiz_id,
                    quiz_name=quiz_name,
                    quiz_description=quiz_description)
        quiz.save()
    return True
