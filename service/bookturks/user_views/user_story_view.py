"""
User Story View
"""
from django.shortcuts import render

from service.bookturks.Constants import USER_STORY_HOME_PAGE, REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE
from service.bookturks.alerts import init_alerts


def user_story_home_view(request):
    """
    User write a story home page.
    :param request:
    :return:
    """
    request, alert_type, alert_message = init_alerts(request=request)

    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type,
    }

    return render(request, USER_STORY_HOME_PAGE, context)
