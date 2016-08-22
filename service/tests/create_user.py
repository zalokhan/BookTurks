from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from service.tests.constants_models import context, mock_user_profile_model


def create_user():
    """
    Creates user for client
    :return: return logged in client
    """
    User.objects.create_user(username=context.get('username'), email=context.get('username'),
                             password=context.get('password'))
    user = authenticate(username=context.get('username'), password=context.get('password'))
    return user


def prepare_client(client):
    """
    Prepare client by loading session objects
    :param client:
    :return:
    """
    session = client.session
    session['user_profile_model'] = mock_user_profile_model
    session.save()
    return client
