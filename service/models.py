"""
Models
"""
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class User(models.Model):
    """
    Basic user details:
    userid
    first and last names
    email
    phone
    dob
    account creation date and time
    """
    username = models.EmailField(max_length=100)
    user_first_name = models.CharField(max_length=50)
    user_last_name = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=20)
    user_dob = models.CharField(max_length=20)
    user_creation_datetime = models.DateTimeField('creation datetime', default=timezone.now)

    # To print out the model in a readable format
    def __str__(self):
        model_string = "EMAIL:" + self.username + "; " + \
                       "FIRSTNAME:" + self.user_first_name + "; " + \
                       "LASTNAME:" + self.user_last_name + "; " + \
                       "PHONE:" + self.user_phone + "; " + \
                       "DOB:" + self.user_dob + "; " + \
                       "CREATE_DATETIME:" + str(self.user_creation_datetime) + "; "
        return model_string


class Quiz(models.Model):
    """
    Quiz Model
    """
    quiz_id = models.CharField(max_length=200)
    quiz_name = models.CharField(max_length=200)
    quiz_description = models.CharField(max_length=1000)
    quiz_owner = models.ForeignKey('User')
    quiz_creation_datetime = models.DateTimeField('quiz datetime', default=timezone.now)

    def __str__(self):
        model_string = "ID:" + self.quiz_id + "; " + \
                       "NAME:" + self.quiz_name + "; " + \
                       "DESCRIPTION:" + self.quiz_description + "; " + \
                       "OWNER:" + str(self.quiz_owner) + "; " + \
                       "QUIZ_DATETIME:" + str(self.quiz_creation_datetime) + ";"
        return model_string


class QuizTag(models.Model):
    """
    Quiz Tags to categorize the quizzes
    """
    tag_name = models.CharField(max_length=50)
    tagged_quiz = models.ManyToManyField(Quiz)

    def __str__(self):
        return "TAG NAME:{0}".format(str(self.tag_name))
