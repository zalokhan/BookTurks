from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from service.bookturks.Constants import USERNAME, PASSWORD, ALERT_MESSAGE, ALERT_TYPE, DANGER, SERVICE_MAIN_HOME, \
    SERVICE_USER_HOME


def login_check_view(request):
    """
    Checks login authentication result and gives failure alert if unsuccessful
    :param request: user request
    :return: renders a page with context
    """

    username = request.POST.get(USERNAME)
    password = request.POST.get(PASSWORD)

    # Authenticate the user with the provided username and password.
    # Django authentication is used here.
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            # Authentication successful
            auth_login(request, user)
            return HttpResponseRedirect(reverse(SERVICE_USER_HOME))

        else:
            # Authentication failure as user was disabled.
            # Creating respective alerts.
            message = "This account has been disabled. Contact the admin."
            alert_type = DANGER
            request.session[ALERT_MESSAGE] = message
            request.session[ALERT_TYPE] = alert_type
            return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))

    else:
        # Authentication failure
        # the authentication system was unable to verify the username and password
        message = "The username or password were incorrect."
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME, ))


def logout_view(request):
    """
    Logs out user
    :param request: user request
    :return: renders a page with context
    """

    logout(request)
    return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME, ))
