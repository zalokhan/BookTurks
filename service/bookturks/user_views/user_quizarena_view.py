"""
Arena to attempt quizzes
"""
from django.shortcuts import render

from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.adapters.QuizAdapter import QuizAdapter
from service.bookturks.quiz.QuizTools import QuizTools

from service.bookturks.alerts import init_alerts
from service.bookturks.Constants import REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE, \
    USER_QUIZARENA_HOME_PAGE


def user_quizarena_home_view(request):
    """
    Home page for the quiz arena
    :param request:
    :return:
    """
    request, alert_type, alert_message = init_alerts(request=request)
    quiz_adapter = QuizAdapter()

    quiz_list = quiz_adapter.get_all_models()
    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type,
        'quiz_list': quiz_list
    }

    return render(request, USER_QUIZARENA_HOME_PAGE, context)
