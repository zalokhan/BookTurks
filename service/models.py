"""
Models
"""
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from dateutil.parser import parse
import json


# Create your models here.
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

    def to_json(self):
        """
        Returns a JSon for the model
        :return:
        """
        model = dict()
        model['username'] = self.username
        model['user_first_name'] = self.user_first_name
        model['user_last_name'] = self.user_last_name
        model['user_phone'] = self.user_phone
        model['user_dob'] = self.user_dob
        model['user_creation_datetime'] = str(self.user_creation_datetime)
        return json.dumps(model, ensure_ascii=False)

    @staticmethod
    def from_json(json_object):
        model = json.loads(json_object)
        return User(username=model.get('username'),
                    user_first_name=model.get('user_first_name'),
                    user_last_name=model.get('user_last_name'),
                    user_phone=model.get('user_phone'),
                    user_dob=model.get('user_dob'),
                    user_creation_datetime=parse(model.get('user_creation_datetime')).astimezone(timezone.utc))


class Message(models.Model):
    """
    Model for storing Notification or messages
    """
    receiver = models.ForeignKey('User', on_delete=models.CASCADE, )
    sender = models.CharField(max_length=100)
    message_subject = models.CharField(max_length=200)
    message_body = models.CharField(max_length=1000)
    message_datetime = models.DateTimeField('message datetime')

    def __str__(self):
        model_string = "RECEIVER:" + self.receiver.username + ";" + \
                       "SENDER:" + self.sender + ";" + \
                       "SUBJECT:" + self.message_subject + ";" + \
                       "MESSAGE:" + self.message_body + ";" + \
                       "MESSAGE_DATETIME" + str(self.message_datetime) + ";"
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

    def to_json(self):
        model = dict()
        model['quiz_id'] = self.quiz_id
        model['quiz_name'] = self.quiz_name
        model['quiz_description'] = self.quiz_description
        model['quiz_owner'] = self.quiz_owner.to_json()
        model['quiz_creation_datetime'] = str(self.quiz_creation_datetime)
        return json.dumps(model, ensure_ascii=False)

    @staticmethod
    def from_json(json_object):
        model = json.loads(json_object)
        return Quiz(quiz_id=model.get('quiz_id'),
                    quiz_name=model.get('quiz_name'),
                    quiz_description=model.get('quiz_description'),
                    quiz_owner=User.from_json(model.get('quiz_owner')),
                    quiz_creation_datetime=model.get('quiz_creation_datetime'))
