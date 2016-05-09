from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from dropbox_adapter.DropboxClient import DropboxClient

from Constants import USERNAME, PASSWORD, ALERT_MESSAGE, ALERT_TYPE, DANGER


def main_home_arena(request):
    """
    Main home page
    Sends alerts if registration successful or login failure
    Args:
        request: user request
    Returns:
        renders a page with context
    """

    # Checks if alert message is required to be displayed on the top
    # Alert type is the severity level of the alert box: success(green) or danger(red)
    alert_message = request.session.get(ALERT_MESSAGE)
    alert_type = request.session.get(ALERT_TYPE)

    # Remove the alerts from the request to prevent repetition of alerts on reload of the page
    if 'alert_message' in request.session:
        del request.session[ALERT_MESSAGE]
        del request.session[ALERT_TYPE]

    # Creating context
    context = {
        'request': request,
        'user': request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type
    }

    return render(request, 'service/main_home_page.html', context)


def login_check_arena(request):
    """
    Checks login authentication result and gives failure alert if unsuccessful
    Args:
        request: user request
    Returns:
        renders a page with context
    """
    username = request.POST[USERNAME]
    password = request.POST[PASSWORD]

    # Authenticate the user with the provided username and password.
    # Django authentication is used here.
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            # Authentication successful
            auth_login(request, user)
            return HttpResponseRedirect(reverse('service:user_home'))

        else:
            # Authentication failure as user was disabled.
            # Creating respective alerts.
            message = "This account has been disabled. Contact the admin."
            alert_type = DANGER
            request.session[ALERT_MESSAGE] = message
            request.session[ALERT_TYPE] = alert_type
            return HttpResponseRedirect(reverse('service:main_home'))

    else:
        # Authentication failure
        # the authentication system was unable to verify the username and password
        message = "The username or password were incorrect."
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse('service:main_home', ))


def logout_arena(request):
    """
    Logs out user
    Args:
        request: user request
    Returns:
        renders a page with context
    """
    logout(request)
    return HttpResponseRedirect(reverse('service:main_home', ))
