"""
User Home View
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from service.bookturks.alerts import init_alerts
from service.bookturks.Constants import SERVICE_MAIN_HOME, USER_HOME_PAGE, REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE, \
    DANGER
from service.bookturks.adapters.user_adapter import user_exists, create_new_user


def user_home_main_view(request):
    """
    User Home page. Lands on the dashboard page
    If not authenticated redirects back to main page
    :param request:
    :return: Renders user_home page (dashboard)
    """
    request, alert_type, alert_message = init_alerts(request=request)
    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type
    }

    # User Exists and nothing else required
    if user_exists(request.user):
        return render(request, USER_HOME_PAGE, context)

    # User does not exist but has email field in social authentication
    elif request.user.email and str(request.user.email).strip():
        # Already created user from email address
        username = "".join([str(request.user.pk), request.user.email])
        if user_exists(username):
            return render(request, USER_HOME_PAGE, context)
        # Create user
        else:
            if create_new_user(username=username, first_name=request.user.first_name,
                               last_name=request.user.last_name, phone="", dob=""):
                return render(request, USER_HOME_PAGE, context)
            else:
                message = "Trouble signing in. Contact the support for help !"
                alert_type = DANGER
                request.session[ALERT_MESSAGE] = message
                request.session[ALERT_TYPE] = alert_type
                return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))

    # User not present and no email field (facebook) so creating username from username and pk
    else:
        username = "".join([str(request.user.pk), request.user.username, "@bookturks.com"])
        if user_exists(request.user.email):
            return render(request, USER_HOME_PAGE, context)
        else:
            if create_new_user(username=username, first_name=request.user.first_name,
                               last_name=request.user.last_name, phone="", dob=""):
                return render(request, USER_HOME_PAGE, context)
            else:
                message = "Trouble signing in. Contact the support for help !"
                alert_type = DANGER
                request.session[ALERT_MESSAGE] = message
                request.session[ALERT_TYPE] = alert_type
                return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))
