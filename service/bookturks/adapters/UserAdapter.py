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

    def create_and_save_model(self, username, first_name="", last_name="", phone="", dob=""):
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

    def create_model(self, username, first_name="", last_name="", phone="", dob=""):
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

    def exists(self, username):
        """
        Checks if user present
        :param quiz_id:
        :return:
        """
        try:
            user = get_object_or_404(User, username=username)
            return user
        except Http404:
            return None

    def get_user_instance_from_request(self, request):
        """
        Fetches User model
        :param request:
        :return:
        """
        # User Exists and nothing else required
        if self.exists(request.user):
            return self.exists(request.user)

        # User does not exist but has email field in social authentication
        elif request.user.email and str(request.user.email).strip():
            username = "".join([str(request.user.pk), request.user.email])
            if self.exists(username):
                return self.exists(username)

        # User not present and no email field (facebook) so creating username from username and pk
        else:
            username = "".join([str(request.user.pk), request.user.username, "@bookturks.com"])
            if self.exists(username):
                return self.exists(username)
            else:
                return None
