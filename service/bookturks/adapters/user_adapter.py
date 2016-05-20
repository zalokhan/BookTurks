from django.shortcuts import get_object_or_404
from django.http import Http404
from service.models import User


def user_exists(username):
    """
    Checks if user present in database
    :param username:
    :return:
    """
    try:
        user = get_object_or_404(User, username=username)
        return user
    except Http404:
        return None


def create_new_user(username, first_name, last_name, phone, dob):
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
        return False
    try:
        get_object_or_404(User, username=username)
    except Http404:
        user = User(username=username,
                    user_first_name=first_name,
                    user_last_name=last_name,
                    user_phone=phone,
                    user_dob=dob)
        user.save()
    return True


def get_user_instance_from_request(request):
    """
    Fetches User model
    :param request:
    :return:
    """
    # User Exists and nothing else required
    if user_exists(request.user):
        return user_exists(request.user)

    # User does not exist but has email field in social authentication
    elif request.user.email and str(request.user.email).strip():
        username = "".join([str(request.user.pk), request.user.email])
        if user_exists(username):
            return user_exists(username)

    # User not present and no email field (facebook) so creating username from username and pk
    else:
        username = "".join([str(request.user.pk), request.user.username, "@bookturks.com"])
        if user_exists(username):
            return user_exists(username)
        else:
            return None
