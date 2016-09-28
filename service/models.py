"""
Models
"""
from __future__ import unicode_literals

import uuid

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
    username = models.EmailField(max_length=100, verbose_name="Username Email", null=False, blank=False, unique=True)
    user_first_name = models.CharField(max_length=50, verbose_name="First Name", null=False, blank=False)
    user_last_name = models.CharField(max_length=50, verbose_name="Last Name", null=False, blank=False)
    user_phone = models.CharField(max_length=20)
    user_dob = models.CharField(max_length=20)
    user_creation_datetime = models.DateTimeField('creation datetime', default=timezone.now)

    # To print out the model in a readable format
    def __str__(self):
        return self.user_first_name + " " + self.user_last_name + " (" + self.username + ")"


class Quiz(models.Model):
    """
    Quiz Model
    """
    quiz_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    quiz_name = models.CharField(max_length=200, verbose_name="Quiz Name", null=False, blank=False)
    quiz_description = models.TextField(verbose_name="Quiz description", null=False, blank=False)
    quiz_owner = models.ForeignKey(User)
    quiz_creation_datetime = models.DateTimeField('quiz datetime', default=timezone.now)
    event_start = models.DateTimeField(default=timezone.now, null=True)
    event_end = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.quiz_name + "  by " + str(self.quiz_owner.username)


class QuizTag(models.Model):
    """
    Quiz Tags to categorize the quizzes
    """
    tag_name = models.CharField(max_length=50, verbose_name="Quiz Tag Name", null=False, blank=False)
    tagged_quiz = models.ManyToManyField(Quiz)

    def __str__(self):
        return "Tag Name: " + self.tag_name
