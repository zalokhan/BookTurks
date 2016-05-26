"""
My quizzes page
"""
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.adapters.QuizAdapter import QuizAdapter
from service.bookturks.quiz.QuizTools import QuizTools

from service.bookturks.alerts import init_alerts, set_alert_session
from service.bookturks.Constants import REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE, DANGER, \
    USER_MYQUIZ_HOME_PAGE, USER_MYQUIZ_INFO_PAGE, SERVICE_USER_HOME, SERVICE_USER_MYQUIZ_HOME


def user_myquiz_home_view(request):
    """
    My quizzes home page
    :param request: User request
    :return: Renders page
    """
    request, alert_type, alert_message = init_alerts(request=request)
    user_adapter = UserAdapter()
    quiz_adapter = QuizAdapter()

    user = user_adapter.get_user_instance_from_request(request)

    quiz_list = quiz_adapter.get_models_for_owner(user_model=user)
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
    user_adapter = UserAdapter()
    quiz_adapter = QuizAdapter()
    quiz_tools = QuizTools()

    user = user_adapter.get_user_instance_from_request(request)
    quiz = quiz_adapter.exists(quiz_id)
    if not quiz or not user:
        set_alert_session(session=request.session,
                          message="No such quiz exists",
                          alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_HOME))

    # Check if this user is the owner of this quiz
    if user != quiz.quiz_owner:
        set_alert_session(session=request.session, message="You do not own this quiz. You are not allowed to edit this",
                          alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_HOME))

    # Downloading the content from storage.
    content = quiz_tools.download_quiz_content(quiz_model=quiz)
    if not content:
        set_alert_session(session=request.session, message="This quiz is unavailable", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_MYQUIZ_HOME))

    # Passing these session objects as this page submits the result to user_quiz_create view which checks for them.
    request.session['quiz_form'] = content['quiz_form']
    request.session['quiz_data'] = content['quiz_data']
    request.session['quiz'] = quiz

    context = {'quiz_data': content['quiz_data']}
    return render(request, USER_MYQUIZ_INFO_PAGE, context)
