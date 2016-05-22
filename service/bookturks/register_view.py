"""
Registration handling
"""
from django.http import HttpResponseRedirect
from django.http import Http404

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from service.bookturks.alerts import init_alerts, set_alert_session
from service.bookturks.Constants import USERNAME, PASSWORD, REPASSWORD, USER_FIRST_NAME, USER_LAST_NAME, USER_PHONE, \
    USER_DOB, \
    ALERT_MESSAGE, ALERT_TYPE, DANGER, SUCCESS, \
    SERVICE_REGISTER, SERVICE_MAIN_HOME, REGISTER_PAGE

from service.bookturks.adapters.UserAdapter import UserAdapter
from service.models import User as UserModel


def register_view(request):
    """
    Register
    Returns page when user clicks the register button or redirected from invalid registration
    :param request: User request
    :return: Renders page
    """
    request, alert_type, alert_message = init_alerts(request=request)
    return render(request, REGISTER_PAGE, {ALERT_MESSAGE: alert_message, ALERT_TYPE: alert_type})


def register_check_view(request):
    """
    Register validation
    Validates the input by the user and checks for duplicates or invalid inputs.
    :param request: User request
    :return: redirects depending on result of authentication.
    """
    # Get all the inputs from the POST method
    username = request.POST.get(USERNAME)
    user_first_name = request.POST.get(USER_FIRST_NAME)
    user_last_name = request.POST.get(USER_LAST_NAME)
    user_phone = request.POST.get(USER_PHONE)
    user_dob = request.POST.get(USER_DOB)
    password = request.POST.get(PASSWORD)
    repassword = request.POST.get(REPASSWORD)

    # Check if none of these are None
    if not username or \
            not user_first_name or \
            not user_last_name or \
            not user_phone or \
            not user_dob or \
            not password or \
            not repassword:
        # Set the alerts in the session field of the request and redirect back to register
        set_alert_session(session=request.session, message="Please fill in all the values", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_REGISTER))

    # Check if passwords are entered properly
    if password != repassword:
        set_alert_session(session=request.session, message="The password should be same in both the fields",
                          alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_REGISTER))

    # The username should be an email address.
    # TODO: We can remove this as javascript on the front end takes care of this.
    if '@' not in username:
        set_alert_session(session=request.session, message="The username should be your email address",
                          alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_REGISTER))

    user_adapter = UserAdapter()

    # Check if username already registered. If yes redirect with warning
    if user_adapter.exists(username):
        set_alert_session(session=request.session, message="User ID already present", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_REGISTER))

    # Creating user in django authentication in database
    auth_user = User.objects.create_user(username=username, email=username, password=password)

    # Set the name in the django authentication
    auth_user.first_name = user_first_name
    auth_user.last_name = user_last_name
    auth_user.save()

    # Creates model and saves to the database.
    user_adapter.create_and_save_model(username=username,
                                       first_name=user_first_name,
                                       last_name=user_last_name,
                                       phone=user_phone,
                                       dob=user_dob)
    set_alert_session(session=request.session,
                      message=" ".join([user_first_name, user_last_name, "registered successfully"]),
                      alert_type=SUCCESS)
    return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))
