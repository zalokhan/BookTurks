"""
Registration handling
"""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from service.bookturks.Constants import USERNAME, PASSWORD, REPASSWORD, USER_FIRST_NAME, USER_LAST_NAME, USER_PHONE, \
    USER_DOB, \
    ALERT_MESSAGE, ALERT_TYPE, DANGER, SUCCESS, \
    SERVICE_REGISTER, SERVICE_MAIN_HOME, REGISTER_PAGE
from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.alerts import init_alerts, set_alert_session


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

    try:
        # Check if none of these are None
        if not username or \
                not user_first_name or \
                not user_last_name or \
                not user_phone or \
                not user_dob or \
                not password or \
                not repassword:
            # Set the alerts in the session field of the request and redirect back to register
            raise ValueError("Please fill in all the values")

        # Check if passwords are entered properly
        if password != repassword:
            raise ValueError("The password should be same in both the fields")

        user_adapter = UserAdapter()

        # Check if username already registered. If yes redirect with warning
        if user_adapter.exists(username):
            raise ValueError("User ID already present")

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
    except ValueError as err:
        set_alert_session(session=request.session,
                          message=str(err),
                          alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_REGISTER))

    set_alert_session(session=request.session,
                      message=" ".join([user_first_name, user_last_name, "registered successfully"]),
                      alert_type=SUCCESS)
    return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))
