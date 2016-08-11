from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone

from service.bookturks.models.NotificationModel import NotificationModel
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

mock_quiz_data = "<form-template>\r\n\t<fields>\r\n\t\t<field class=\"header\" label=\"Header\" type=\"header\" " \
                 "subtype=\"h1\"></field>\r\n\t\t<field class=\"form-control select\" label=\"Select\" multiple=\"" \
                 "true\" name=\"select-1464031178941\" type=\"select\">\r\n\t\t\t<option value=\"option-1\">" \
                 "Physics</option>\r\n\t\t\t<option value=\"option-2\">Biology</option>\r\n\t\t\t<option>Chemistry" \
                 "</option>\r\n\t\t\t<option>History</option>\r\n\t\t\t<option>English</option>\r\n\t\t</field>\r\n" \
                 "\t</fields>\r\n</form-template>"

mock_quiz_form = "<div class=\"\"><h1>Header</h1></div><div class=\"form-group field-select-1464031178941\"><label " \
                 "for=\"select-1464031178941\">Select  </label><select class=\"form-control select\" multiple=\"" \
                 "true\" name=\"select-1464031178941\" type=\"select\" id=\"select-1464031178941\"><option value=\"" \
                 "option-1\">Physics</option><option value=\"option-2\">Biology</option><option>Chemistry</option>" \
                 "<option>History</option><option>English</option></select></div>"

mock_quiz_complete_model = QuizCompleteModel(quiz_model=mock_quiz_model,
                                             answer_key={"select-1464031178941": ["option-1", "option-2", "Chemistry"]},
                                             quiz_data=mock_quiz_data,
                                             quiz_form=mock_quiz_form,
                                             pass_percentage=100)

mock_user_profile_model = UserProfileModel(user_model=mock_user_model,
                                           notifications=[NotificationModel(sender="BookTurks",
                                                                            level=NotificationModel.Level.SUCCESS,
                                                                            message="Congratulations",
                                                                            time=timezone.now()),
                                                          NotificationModel(sender="BookTurks",
                                                                            level=NotificationModel.Level.INFO,
                                                                            message="Unfinished items",
                                                                            time=timezone.now())],
                                           my_quiz=[mock_quiz_model],
                                           attempted_quiz=[])


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
