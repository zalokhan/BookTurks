from django.http import Http404
from django.shortcuts import get_object_or_404

from service.models import Quiz


class QuizAdapter(object):
    """
    Quiz Adapter
    """

    def __init__(self):
        """
        Creates quiz adapter object
        """
        pass

    @staticmethod
    def create_and_save_model(quiz_name, quiz_description, quiz_owner, start_time=None, end_time=None):
        """
        Creates and saves quiz object
        :param quiz_name:
        :param quiz_description:
        :param quiz_owner:
        :param start_time:
        :param end_time:
        :return:
        """
        quiz = QuizAdapter.create_model(quiz_name, quiz_description, quiz_owner, start_time, end_time)
        quiz.save()
        return quiz

    @staticmethod
    def create_model(quiz_name, quiz_description, quiz_owner, start_time=None, end_time=None):
        """
        Creates model
        :param quiz_name:
        :param quiz_description:
        :param quiz_owner:
        :param start_time:
        :param end_time:
        :return:
        """
        if not quiz_name or not quiz_name.strip() or \
                not quiz_description or not quiz_description.strip() or \
                not quiz_owner:
            raise ValueError("Quiz model cannot be created. Parameter missing.")

        quiz = QuizAdapter.get_quiz_for_owner(quiz_owner, quiz_name)
        if quiz:
            raise ValueError("Quiz already present")

        quiz = Quiz(quiz_name=quiz_name, quiz_description=quiz_description, quiz_owner=quiz_owner,
                    event_start=start_time, event_end=end_time)
        return quiz

    @staticmethod
    def exists(quiz_id):
        """
        Checks if quiz present
        :param quiz_id:
        :return:
        """
        try:
            quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
            return quiz
        except Http404:
            return None

    @staticmethod
    def delete_model(quiz):
        """
        Deletes model from database
        :param quiz:
        :return:
        """
        if quiz and quiz.quiz_id and QuizAdapter.exists(quiz.quiz_id):
            quiz.delete()

    @staticmethod
    def get_models_for_owner(user_model):
        """
        Returns a list of all quizzes owned by the user passed in the argument
        :param user_model:
        :return:
        """
        return Quiz.objects.filter(quiz_owner=user_model)

    @staticmethod
    def get_quiz_for_owner(user, quiz_name):
        """
        Returns the quiz owned by the user passed in the argument
        :param user:
        :param quiz_name:
        :return:
        """
        # iexact is for making the quiz name case insensitive
        return Quiz.objects.filter(quiz_name__iexact=quiz_name, quiz_owner=user)

    @staticmethod
    def get_all_models():
        """
        Returns list of all quizzes
        :return:
        """
        return Quiz.objects.all()
