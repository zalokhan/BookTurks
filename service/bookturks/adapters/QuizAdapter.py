from django.shortcuts import get_object_or_404
from django.http import Http404
from service.models import Quiz
from service.bookturks.adapters.AbstractAdapter import AbstractAdapter


class QuizAdapter(AbstractAdapter):
    """
    Quiz Adapter
    """

    def __init__(self):
        """
        Creates quiz adapter object
        """
        pass

    def create_and_save_model(self, quiz_id, quiz_name, quiz_description, quiz_owner):
        """
        Creates and saves quiz object
        :param quiz_id:
        :param quiz_name:
        :param quiz_description:
        :param quiz_owner:
        :return:
        """
        if not quiz_id or not quiz_id.strip() or \
                not quiz_name or not quiz_name.strip() or \
                not quiz_description or not quiz_description.strip() or \
                not quiz_owner:
            return None
        try:
            get_object_or_404(Quiz, quiz_id=quiz_id)
            return None
        except Http404:
            quiz = Quiz(quiz_id=quiz_id, quiz_name=quiz_name, quiz_description=quiz_description, quiz_owner=quiz_owner)
            quiz.save()
        return quiz

    def create_model(self, quiz_id, quiz_name, quiz_description, quiz_owner):
        """
        Creates model
        :param quiz_id:
        :param quiz_name:
        :param quiz_description:
        :param quiz_owner:
        :return:
        """
        if not quiz_id or not quiz_id.strip() or \
                not quiz_name or not quiz_name.strip() or \
                not quiz_description or not quiz_description.strip() or \
                not quiz_owner:
            return None
        try:
            get_object_or_404(Quiz, quiz_id=quiz_id)
            return None
        except Http404:
            quiz = Quiz(quiz_id=quiz_id, quiz_name=quiz_name, quiz_description=quiz_description, quiz_owner=quiz_owner)
        return quiz

    def exists(self, quiz_id):
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

    def get_models_for_owner(self, user_model):
        """
        Returns a list of all quizzes owned by the user passed in the argument
        :param user_model:
        :return:
        """
        return Quiz.objects.filter(quiz_owner=user_model)

    def get_all_models(self):
        """
        Returns list of all quizzes
        :return:
        """
        return Quiz.objects.all()
