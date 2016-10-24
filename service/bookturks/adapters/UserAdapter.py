from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import models

from service.models import User


class UserAdapter(object):
    """
    User Adapter
    """

    def __init__(self):
        """
        Creates user adapter object
        """
        pass

    @staticmethod
    def create_and_save_model(username, first_name="", last_name="", phone="", dob=""):
        """
        Creates and saves new user for the database
        :param username:
        :param first_name:
        :param last_name:
        :param phone:
        :param dob:
        :return: True if new user created or already present else false
        """
        user = UserAdapter.create_model(username, first_name, last_name, phone, dob)
        user.save()
        return user

    @staticmethod
    def create_model(username, first_name="", last_name="", phone="", dob=""):
        """
        Creates new user for the database
        :param username:
        :param first_name:
        :param last_name:
        :param phone:
        :param dob:
        :return: True if new user created or already present else false
        """
        if not username or not username.strip():
            raise ValueError("User model cannot be created. Parameter missing.")
        if UserAdapter.exists(username=username):
            raise ValueError("User Model already present")
        else:
            user = User(username=username,
                        user_first_name=first_name,
                        user_last_name=last_name,
                        user_phone=phone,
                        user_dob=dob)
        return user

    @staticmethod
    def exists(username):
        """
        Checks if user present
        :param username:
        :return:
        """
        try:
            user = get_object_or_404(User, username=username)
            return user
        except Http404:
            return None

    @staticmethod
    def get_user_instance_from_django_user(user):
        """
        Fetches User model
        :param user:
        :return:
        """

        # User Exists and nothing else required
        if UserAdapter.exists(user):
            return UserAdapter.exists(user)

        # User does not exist but has email field in social authentication
        elif user.email and str(user.email).strip():
            username = user.email
            if UserAdapter.exists(username):
                return UserAdapter.exists(username)

        # User not present and no email field (facebook) so creating username from username and pk
        else:
            username = "".join([user.username, "@bookturks.com"])
            if UserAdapter.exists(username):
                return UserAdapter.exists(username)
            else:
                return None

    @staticmethod
    def get_user_from_django(email):
        """
        Fetches User model from django user using email
        :param email:
        :return:
        """
        if not email or not email.strip():
            raise ValueError("User model cannot be created. Parameter missing.")
        try:
            user = models.User.objects.get(email=email)
        except Http404:
            raise(Http404, "User not found.")
        return user

    @staticmethod
    def get_user_from_django_pk(pk):
        """
        Fetches User model from django user using pk
        :param pk:
        :return:
        """
        if not pk or not pk.strip():
            raise ValueError("User model cannot be created. Parameter missing.")
        try:
            user = models.User.objects.get(pk=pk)
        except Http404:
            raise(Http404, "User not found.")
        return user

    @staticmethod
    def user_change_password(user, password):
        """
            Changes the Django user password
            :param user:
            :param password:
            :return:
            """
        if not password:
            raise ValueError("Value for password must be provided")
        user.set_password(password)
        user.save()
        return user

