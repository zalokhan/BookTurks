"""
Arena to attempt quizzes
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from service.bookturks.adapters.QuizAdapter import QuizAdapter
from service.bookturks.quiz.QuizTools import QuizTools

from service.bookturks.alerts import init_alerts, set_alert_session
from service.bookturks.Constants import REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE, DANGER, \
    USER_QUIZARENA_HOME_PAGE, SERVICE_USER_QUIZARENA_HOME, USER_QUIZARENA_SOLVE_PAGE, USER_QUIZARENA_RESULT_PAGE


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


def user_quizarena_solve_view(request, quiz_id):
    """
    Attempt the quiz here. Setup for the player to attempt.
    Disallow repeated attempts.
    :param request:
    :param quiz_id:
    :return:
    """
    request, alert_type, alert_message = init_alerts(request=request)
    quiz_adapter = QuizAdapter()
    quiz_tools = QuizTools()

    quiz = quiz_adapter.exists(quiz_id)
    if not quiz:
        set_alert_session(session=request.session, message="No such quiz present", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZARENA_HOME))
    content = quiz_tools.download_quiz_content(quiz_model=quiz)

    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type,
        'quiz_form': content.get('quiz_form')
    }
    request.session['quiz'] = quiz

    return render(request, USER_QUIZARENA_SOLVE_PAGE, context)


def user_quizarena_result_view(request):
    """
    Result of the quiz attempt
    :param request:
    :return:
    """
    request, alert_type, alert_message = init_alerts(request=request)
    quiz = request.session.get('quiz')

    if not quiz:
        set_alert_session(session=request.session, message="Invalid quiz attempt. No such quiz.", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZARENA_HOME))

    quiz_tools = QuizTools()
    content = quiz_tools.download_quiz_content(quiz_model=quiz)
    answer_key = content.get('answer_key')
    user_answer_key = dict(request.POST)
    if 'csrfmiddlewaretoken' in user_answer_key:
        del user_answer_key['csrfmiddlewaretoken']

    right = 0
    wrong = 0
    for key in answer_key.keys():
        print user_answer_key.get(key)
        print answer_key.get(key)
        if not user_answer_key.get(key) and not answer_key.get(key):
            continue
        if user_answer_key.get(key) == answer_key.get(key):
            right += 1
        else:
            wrong += 1

    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type,
        'right': right,
        'wrong': wrong
    }

    del request.session['quiz']
    return render(request, USER_QUIZARENA_RESULT_PAGE, context)
