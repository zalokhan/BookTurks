"""
My quizzes page
"""
from django.shortcuts import render

from service.bookturks.adapters.user_adapter import get_user_instance_from_request
from service.bookturks.adapters.quiz_adapter import quiz_exists

from service.bookturks.alerts import init_alerts
from service.bookturks.Constants import REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE, \
    USER_MYQUIZ_HOME_PAGE
from service.models import Quiz


def user_myquiz_home_view(request):
    """
    My quizzes home page
    :param request: User request
    :return: Renders page
    """
    request, alert_type, alert_message = init_alerts(request=request)

    user = get_user_instance_from_request(request)

    quiz_list = Quiz.objects.filter(quiz_owner=user)
    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type,
        'quiz_list': quiz_list
    }

    return render(request, USER_MYQUIZ_HOME_PAGE, context)
