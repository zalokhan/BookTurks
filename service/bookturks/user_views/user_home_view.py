"""
User Home View
"""
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

from service.bookturks.alerts import init_alerts
from service.bookturks.Constants import SERVICE_MAIN_HOME, USER_HOME_PAGE, REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE


def user_home_main_view(request):
    """
    User Home page. Lands on the dashboard page
    If not authenticated redirects back to main page
    :param request:
    :return: Renders user_home page (dashboard)
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))
    request, alert_type, alert_message = init_alerts(request=request)
    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type
    }

    return render(request, USER_HOME_PAGE, context)
