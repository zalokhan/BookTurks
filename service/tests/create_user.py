import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from service.models import User as UserModel
from service.bookturks.models.UserProfileModel import UserProfileModel

context = {
    'username': 'test@email.com',
    'user_first_name': 'testfirstname',
    'user_last_name': 'testlastname',
    'user_phone': '1234567890',
    'user_dob': '01/01/1990',
    'password': 'test',
    'repassword': 'test'
}

mock_user_profile_model_json = {
    "notifications":
        ["{\"message\": \"Congratulations on your new Account !\", \"time\": \"2016-06-15 06:49:47.528282+00:00\", "
         "\"sender\": \"BookTurks\", \"level\": \"SUCCESS\"}",
         "{\"message\": \"You have unfinished items in your profile\", \"time\": \"2016-06-15 06:49:47.528300+00:00\", "
         "\"sender\": \"BookTurks\", \"level\": \"INFO\"}"],
    "user_model":
        "{\"username\": \"test@email.com\", \"user_creation_datetime\": "
        "\"2016-06-05 21:12:37.467760+00:00\", \"user_phone\": \"\", \"user_first_name\": \"testfirstname\", "
        "\"user_last_name\": \"testlastname\", \"user_dob\": \"\"}",
    "attempted_quiz": [],
    "display_picture": "",
    "my_quiz": ["{\"quiz_creation_datetime\": \"2016-06-15 06:47:23.920834+00:00\", \"quiz_id\": "
                "\"testemailcomTestQuiz\", \"quiz_description\": \"Test Quiz Dev\", "
                "\"quiz_name\": \"Test Quiz\", \"quiz_owner\": \"{\\\"username\\\": "
                "\\\"test@email.com\\\", \\\"user_creation_datetime\\\": "
                "\\\"2016-06-05 21:12:37.467760+00:00\\\", \\\"user_phone\\\": \\\"1234567890\\\", "
                "\\\"user_first_name\\\": \\\"testfirstname\\\", \\\"user_last_name\\\": \\\"testlastname\\\", "
                "\\\"user_dob\\\": \\\"01/01/1990\\\"}\"}"]}

mock_user_profile_model = UserProfileModel.from_json(json.dumps(mock_user_profile_model_json, ensure_ascii=False))


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
