"""
My quizzes page
"""
from django.shortcuts import render

from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.adapters.QuizAdapter import QuizAdapter
from service.bookturks.quiz.QuizTools import QuizTools

from service.bookturks.alerts import init_alerts
from service.bookturks.Constants import REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE, \
    USER_MYQUIZ_HOME_PAGE, USER_MYQUIZ_INFO_PAGE
from service.models import Quiz


def user_myquiz_home_view(request):
    """
    My quizzes home page
    :param request: User request
    :return: Renders page
    """
    request, alert_type, alert_message = init_alerts(request=request)
    user_adapter = UserAdapter()

    user = user_adapter.get_user_instance_from_request(request)

    quiz_list = Quiz.objects.filter(quiz_owner=user)
    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type,
        'quiz_list': quiz_list
    }

    return render(request, USER_MYQUIZ_HOME_PAGE, context)


def user_myquiz_info_view(request, quiz_id):
    """
    Quiz related tasks
    :param request:
    :param quiz_id:
    :return:
    """
    quiz_adapter = QuizAdapter()
    quiz_tools = QuizTools()

    quiz = quiz_adapter.exists(quiz_id)
    # TODO: DO something if quiz does not exist

    content = quiz_tools.download_quiz_content(quiz_model=quiz)

    request.session['quiz_form'] = content['quiz_form']
    request.session['quiz_data'] = content['quiz_data']
    request.session['quiz'] = quiz
    context = {
        'quiz_data': content['quiz_data']
    }

    return render(request, USER_MYQUIZ_INFO_PAGE, context)
