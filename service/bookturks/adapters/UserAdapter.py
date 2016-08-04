from django.shortcuts import get_object_or_404
from django.http import Http404
from service.models import User
from service.bookturks.adapters.AbstractAdapter import AbstractAdapter


class UserAdapter(AbstractAdapter):
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
        if not username or not username.strip():
            return None
        try:
            get_object_or_404(User, username=username)
            return None
        except Http404:
            user = User(username=username,
                        user_first_name=first_name,
                        user_last_name=last_name,
                        user_phone=phone,
                        user_dob=dob)
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
            return None
        try:
            get_object_or_404(User, username=username)
            return None
        except Http404:
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
    def get_user_instance_from_request(request):
        """
        Fetches User model
        :param request:
        :return:
        """
        # User Exists and nothing else required
        if UserAdapter.exists(request.user):
            return UserAdapter.exists(request.user)

        # User does not exist but has email field in social authentication
        elif request.user.email and str(request.user.email).strip():
            username = "".join([str(request.user.pk), request.user.email])
            if UserAdapter.exists(username):
                return UserAdapter.exists(username)

        # User not present and no email field (facebook) so creating username from username and pk
        else:
            username = "".join([str(request.user.pk), request.user.username, "@bookturks.com"])
            if UserAdapter.exists(username):
                return UserAdapter.exists(username)
            else:
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
            username = "".join([str(user.pk), user.email])
            if UserAdapter.exists(username):
                return UserAdapter.exists(username)

        # User not present and no email field (facebook) so creating username from username and pk
        else:
            username = "".join([str(user.pk), user.username, "@bookturks.com"])
            if UserAdapter.exists(username):
                return UserAdapter.exists(username)
            else:
                return None
