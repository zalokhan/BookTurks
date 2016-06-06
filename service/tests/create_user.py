from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from service.models import User as UserModel

context = {
    'username': 'test@email.com',
    'user_first_name': 'testfirstname',
    'user_last_name': 'testlastname',
    'user_phone': '1234567890',
    'user_dob': '01/01/1990',
    'password': 'test',
    'repassword': 'test'
}


def create_user():
    """
    Creates user for client
    :return: return logged in client
    """
    User.objects.create_user(username=context.get('username'), email=context.get('username'),
                             password=context.get('password'))
    user = authenticate(username=context.get('username'), password=context.get('password'))
    return user


def create_user_model_in_database():
    """
    Creates a test user in the database from the above context
    :return:
    """
    user = UserModel(username=context.get('username'),
                     user_first_name=context.get('user_first_name'),
                     user_last_name=context.get('user_last_name'),
                     user_phone=context.get('user_phone'),
                     user_dob=context.get('user_dob'))
    user.save()
    return user
