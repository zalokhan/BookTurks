"""
User Home View
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from service.bookturks.alerts import init_alerts, set_alert_session
from service.bookturks.Constants import SERVICE_MAIN_HOME, USER_HOME_PAGE, REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE, \
    DANGER
from service.bookturks.adapters.UserAdapter import UserAdapter


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
    user_adapter = UserAdapter()

    # User Exists and nothing else required
    if user_adapter.exists(request.user):
        return render(request, USER_HOME_PAGE, context)

    # User does not exist but has email field in social authentication
    elif request.user.email and str(request.user.email).strip():
        # Creating username from email address
        username = "".join([str(request.user.pk), request.user.email])
        # username exists
        if user_adapter.exists(username):
            return render(request, USER_HOME_PAGE, context)
        # Create user
        else:
            if user_adapter.create_and_save_model(username=username, first_name=request.user.first_name,
                                                  last_name=request.user.last_name, phone="", dob=""):
                return render(request, USER_HOME_PAGE, context)
            # This condition should never be encountered
            else:
                set_alert_session(session=request.session, message="Trouble signing in. Contact the support for help !",
                                  alert_type=DANGER)
                return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))

    # User not present and no email field (facebook) so creating username from username and pk
    else:
        # Creating username from pk and username in auth
        username = "".join([str(request.user.pk), request.user.username, "@bookturks.com"])
        if user_adapter.exists(username):
            return render(request, USER_HOME_PAGE, context)
        else:
            if user_adapter.create_and_save_model(username=username, first_name=request.user.first_name,
                                                  last_name=request.user.last_name, phone="", dob=""):
                return render(request, USER_HOME_PAGE, context)
            else:
                set_alert_session(session=request.session, message="Trouble signing in. Contact the support for help !",
                                  alert_type=DANGER)
                return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))
