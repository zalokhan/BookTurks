import re

from django.http import Http404
from django.shortcuts import get_object_or_404

from service.bookturks.adapters.QuizAdapter import QuizAdapter
from service.models import QuizTag


class QuizTagAdapter(object):
    """
    QuizTag Adapter
    """

    def __init__(self):
        """
        Creates quiz_tag adapter object
        """
        pass

    @staticmethod
    def create_and_save_model(tag_name):
        """
        Creates and saves the model
        :param tag_name:
        :return:
        """
        if not tag_name:
            raise ValueError("tag_name cannot be empty or None")
        if QuizTagAdapter.exists(tag_name):
            raise ValueError("Cannot create new tag. Tag already exists")
        else:
            quiz_tag = QuizTag(tag_name=tag_name)
            quiz_tag.save()
        return quiz_tag

    @staticmethod
    def create_model(tag_name):
        """
        Creates the model
        :param tag_name:
        :return:
        """
        if not tag_name:
            raise ValueError("tag_name cannot be empty or None")
        if QuizTagAdapter.exists(tag_name):
            raise ValueError("Cannot create new tag. Tag already exists")
        else:
            quiz_tag = QuizTag(tag_name=tag_name)
        return quiz_tag

    @staticmethod
    def exists(tag_name):
        """
        Checks if quiz_tag present
        :param tag_name:
        :return:
        """
        try:
            quiz_tag = get_object_or_404(QuizTag, tag_name=tag_name)
            return quiz_tag
        except Http404:
            return None

    @staticmethod
    def delete_model(quiz_tag):
        """
        Deletes model from database
        :param quiz_tag:
        :return:
        """
        if quiz_tag and QuizTagAdapter.exists(quiz_tag.tag_name):
            quiz_tag.delete()

    @staticmethod
    def link_quiz(tag_name, quiz_id):
        """
        Links the tag to this quiz_model
        :param tag_name:
        :param quiz_id:
        :return:
        """
        if not tag_name or \
                not QuizTagAdapter.exists(tag_name) or \
                not QuizAdapter.exists(quiz_id):
            raise ValueError("Tag name invalid or quiz does not exist.")
        quiz_tag = QuizTagAdapter.exists(tag_name)
        quiz_tag.tagged_quiz.add(QuizAdapter.exists(quiz_id))

    @staticmethod
    def unlink_quiz(tag_name, quiz_id):
        """
        Uninks the tag to this quiz_model
        :param tag_name:
        :param quiz_id:
        :return:
        """
        if not tag_name or \
                not QuizTagAdapter.exists(tag_name) or \
                not QuizAdapter.exists(quiz_id):
            raise ValueError("Cannot unlink tag. Invalid tag_name or quiz does not exist.")
        quiz_tag = QuizTagAdapter.exists(tag_name)
        quiz_tag.tagged_quiz.remove(QuizAdapter.exists(quiz_id))
        if not quiz_tag.tagged_quiz.count():
            quiz_tag.delete()

    @staticmethod
    def verify_tag_name(tag_name):
        """
        Verifies the tag_name
        :param tag_name:
        :return:
        """
        return re.match("^[A-Za-z0-9_ .-]*$", tag_name)

    @staticmethod
    def split_and_verify_tag_names(tag_string):
        """
        Splits the tags and then verifies them
        :param tag_string:
        :return:
        """
        if not tag_string:
            return None
        tag_names = tag_string.split(',')
        for tag_name in tag_names:
            if not QuizTagAdapter.verify_tag_name(tag_name):
                raise ValueError("Tag name can only contain alphanumeric characters, spaces, hyphens and underscores")
        return tag_names
