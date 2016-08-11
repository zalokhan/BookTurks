"""
Arena to attempt quizzes
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.adapters.QuizAdapter import QuizAdapter
from service.bookturks.quiz.QuizTools import QuizTools
from service.bookturks.user.UserProfileTools import UserProfileTools

from service.bookturks.alerts import init_alerts, set_alert_session
from service.bookturks.Constants import REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE, DANGER, \
    USER_QUIZARENA_HOME_PAGE, SERVICE_USER_QUIZARENA_HOME, USER_QUIZARENA_SOLVE_PAGE, USER_QUIZARENA_RESULT_PAGE, USER_PROFILE_MODEL


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
    if not content:
        set_alert_session(session=request.session, message="This quiz is unavailable", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZARENA_HOME))

    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type,
        'quiz_form': content.quiz_form
    }
    request.session['quiz'] = content.quiz_model

    return render(request, USER_QUIZARENA_SOLVE_PAGE, context)


def user_quizarena_result_view(request):
    """
    Result of the quiz attempt
    :param request:
    :return:
    """
    request, alert_type, alert_message = init_alerts(request=request)
    quiz = request.session.get('quiz')

    user_adapter = UserAdapter()
    quiz_tools = QuizTools()
    # Get the user model from the request.
    user = user_adapter.get_user_instance_from_request(request)

    if not quiz or not user:
        set_alert_session(session=request.session, message="Invalid quiz attempt.", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZARENA_HOME))

    content = quiz_tools.download_quiz_content(quiz_model=quiz)
    if not content:
        set_alert_session(session=request.session, message="This quiz is unavailable", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZARENA_HOME))

    answer_key = content.answer_key
    user_answer_key = dict(request.POST)

    quiz_result_model = quiz_tools.get_quiz_result(user_model=user, quiz_model=quiz, answer_key=answer_key,
                                                   user_answer_key=user_answer_key)
    # Save result in model
    UserProfileTools.save_attempted_quiz_profile(session=request.session, quiz_result_model=quiz_result_model)
    # Save the profile
    user_profile_tools = UserProfileTools()
    future = user_profile_tools.save_profile(request.session)

    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type,
        'result': quiz_result_model
    }

    # Clearing the session
    del request.session['quiz']

    # Wait for asynchronous callback
    future.result()
    return render(request, USER_QUIZARENA_RESULT_PAGE, context)
