import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from service.bookturks.models.QuizCompleteModel import QuizCompleteModel
from service.bookturks.models.UserProfileModel import UserProfileModel
from service.models import Quiz
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

mock_user_model = UserModel(
    username='test@email.com',
    user_first_name='testfirstname',
    user_last_name='testlastname',
    user_phone='1234567890',
    user_dob='01/01/1990')

mock_quiz_model = Quiz(quiz_id='test_quiz_id',
                       quiz_name='test_quiz_name',
                       quiz_description='test_quiz_description',
                       quiz_owner=mock_user_model)

mock_quiz_complete_model = QuizCompleteModel(quiz_model=mock_quiz_model,
                                             answer_key={"select-1464031178941": ["option-1", "option-2", "Chemistry"]},
                                             event_model=None,
                                             quiz_data="<form-template>\r\n\t<fields>\r\n\t\t<field class=\"header\" "
                                                       "label=\"Header\" type=\"header\" subtype=\"h1\"></field>\r\n\t"
                                                       "\t<field class=\"form-control select\" label=\"Select\" "
                                                       "multiple=\"true\" name=\"select-1464031178941\" type=\""
                                                       "select\">\r\n\t\t\t<option value=\"option-1\">Physics"
                                                       "</option>\r\n\t\t\t<option value=\"option-2\">Biology"
                                                       "</option>\r\n\t\t\t<option>Chemistry</option>\r\n\t\t\t<option>"
                                                       "History</option>\r\n\t\t\t<option>English</option>\r\n\t\t"
                                                       "</field>\r\n\t</fields>\r\n</form-template>",
                                             quiz_form="<div class=\"\"><h1>Header</h1></div><div class=\"form-group "
                                                       "field-select-1464031178941\"><label for=\"select-1464031178941"
                                                       "\">Select  </label><select class=\"form-control select\" "
                                                       "multiple=\"true\" name=\"select-1464031178941\" type=\"select"
                                                       "\" id=\"select-1464031178941\"><option value=\"option-1\">"
                                                       "Physics</option><option value=\"option-2\">Biology</option>"
                                                       "<option>Chemistry</option><option>History</option><option>"
                                                       "English</option></select></div>",
                                             pass_percentage=100)

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
