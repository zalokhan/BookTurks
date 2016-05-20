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
    username = request.POST.get(USERNAME)
    user_first_name = request.POST.get(USER_FIRST_NAME)
    user_last_name = request.POST.get(USER_LAST_NAME)
    user_phone = request.POST.get(USER_PHONE)
    user_dob = request.POST.get(USER_DOB)
    password = request.POST.get(PASSWORD)
    repassword = request.POST.get(REPASSWORD)

    if not username or \
            not user_first_name or \
            not user_last_name or \
            not user_phone or \
            not user_dob or \
            not password or \
            not repassword:
        message = "Please fill in all the values"
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_REGISTER))

    if password != repassword:
        message = "The password should be same in both the fields"
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_REGISTER))

    if '@' not in username:
        message = "The username should be your email address"
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_REGISTER))

    try:
        get_object_or_404(UserModel, username=username)
    except Http404:
        # Creating user in django authentication
        auth_user = User.objects.create_user(username=username, email=username, password=password)
    else:
        message = "User ID already present"
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_REGISTER))

    auth_user.first_name = user_first_name
    auth_user.last_name = user_last_name
    auth_user.save()

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
