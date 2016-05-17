"""
Registration handling
"""
from django.http import HttpResponseRedirect
from django.http import Http404

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from service.bookturks.alerts import init_alerts
from service.bookturks.Constants import USERNAME, PASSWORD, REPASSWORD, USER_FIRST_NAME, USER_LAST_NAME, USER_PHONE, \
    USER_DOB, \
    ALERT_MESSAGE, ALERT_TYPE, DANGER, SUCCESS, \
    SERVICE_REGISTER, SERVICE_MAIN_HOME, REGISTER_PAGE

from service.models import User as UserModel


def register_arena(request):
    """
    Register
    Returns page when user clicks the register button or redirected from invalid registration
    :param request: User request
    :return: Renders page
    """
    request, alert_type, alert_message = init_alerts(request=request)
    return render(request, REGISTER_PAGE, {ALERT_MESSAGE: alert_message, ALERT_TYPE: alert_type})


def register_check_arena(request):
    """
    Register validation
    Validates the input by the user and checks for duplicates or invalid inputs.
    :param request: User request
    :return: redirects depending on result of authentication.
    """
    username = request.POST[USERNAME]
    user_first_name = request.POST[USER_FIRST_NAME]
    user_last_name = request.POST[USER_LAST_NAME]
    user_phone = request.POST[USER_PHONE]
    user_dob = request.POST[USER_DOB]
    password = request.POST[PASSWORD]
    repassword = request.POST[REPASSWORD]

    if username is None or \
                    user_first_name is None or \
                    user_last_name is None or \
                    user_phone is None or \
                    user_dob is None or \
                    password is None or \
                    password != repassword:
        message = "The password should be same in both the fields"
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_REGISTER))

    try:
        get_object_or_404(UserModel, username=username)
    except Http404:
        # Creating user in django authentication
        auth_user = User.objects.create_user(username=username, email=username, password=password)
        auth_user.first_name = user_first_name
        auth_user.last_name = user_last_name
    else:
        message = "User ID already present"
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_REGISTER))

    user = UserModel(username=username,
                     user_first_name=user_first_name,
                     user_last_name=user_last_name,
                     user_phone=user_phone,
                     user_dob=user_dob)
    user.save()
    message = " ".join([user_first_name, user_last_name, "registered successfully"])
    alert_type = SUCCESS
    request.session[ALERT_MESSAGE] = message
    request.session[ALERT_TYPE] = alert_type
    return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))
