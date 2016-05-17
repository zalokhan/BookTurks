"""
User account pages
"""
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from service.models import Quiz, User

from alerts import init_alerts
from Constants import SERVICE_MAIN_HOME, SERVICE_USER_QUIZ_INIT, SERVICE_USER_HOME, \
    USER_HOME_PAGE, USER_QUIZ_INIT_PAGE, USER_QUIZ_MAKER_PAGE, USER_QUIZ_VERIFIER_PAGE, \
    REQUEST, USER, \
    ALERT_MESSAGE, ALERT_TYPE, DANGER, SUCCESS
from quiz.QuizMaker import quiz_form_data_parser, create_quiz_content


def user_home_main_arena(request):
    """
    User Home page. Lands on the dashboard page
    If not authenticated redirects back to main page
    :param request:
    :return: Renders user_home page (dashboard)
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))
    request, alert_type, alert_message = init_alerts(request=request)

    return render(request, USER_HOME_PAGE)


def user_quiz_init_arena(request):
    """
    Landing quiz page and verifier and name checker
    :param request: User request
    :return: renders quiz name form
    """

    request, alert_type, alert_message = init_alerts(request=request)
    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type
    }

    return render(request, USER_QUIZ_INIT_PAGE, context)


def user_quiz_maker_arena(request):
    """
    Quiz creation page for user
    :param request: User request
    :return: Renders quiz page
    """
    quiz_id = request.POST.get('quiz_id')
    quiz_name = request.POST.get('quiz_name')
    quiz_description = request.POST.get('quiz_description')

    request, alert_type, alert_message = init_alerts(request=request)

    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type
    }

    if not quiz_id.rstrip():
        message = "The quiz id cannot be empty."
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    try:
        get_object_or_404(Quiz, quiz_id=quiz_id)
    except Http404:
        pass
    else:
        message = "Quiz ID already present"
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    quiz = Quiz(
        quiz_id=quiz_id,
        quiz_name=quiz_name,
        quiz_description=quiz_description,
        quiz_owner=request.user)
    quiz.save()

    message = " ".join([quiz_id, "created successfully"])
    alert_type = SUCCESS
    request.session[ALERT_MESSAGE] = message
    request.session[ALERT_TYPE] = alert_type
    request.session['quiz'] = quiz

    return render(request, USER_QUIZ_MAKER_PAGE, context)


def user_quiz_verifier_arena(request):
    """
    Verifies the form for errors
    Asks the user to prepare the answer key
    :param request: User request
    :return: Message depending on success or failure of quiz creation.
    """
    request, alert_type, alert_message = init_alerts(request=request)
    quiz_form = request.POST.get('quiz_form')
    quiz_data = request.POST.get('quiz_data')

    # TODO: Put try catch and handle exceptions
    quiz_form = quiz_form_data_parser(form_data=quiz_form)

    context = {
        'quiz_form': quiz_form,
    }
    request.session['quiz_form'] = quiz_form
    request.session['quiz_data'] = quiz_data

    return render(request, USER_QUIZ_VERIFIER_PAGE, context)


def user_quiz_create_arena(request):
    """
    Creates the quiz and uploads to storage.
    :param request: User request
    :return: Redirects to dashboard on successful quiz creation.
    """
    answer_key = request.POST

    quiz_form = request.session.get('quiz_form')
    quiz_data = request.session.get('quiz_data')
    quiz = request.session.get('quiz')
    return_code = create_quiz_content(quiz_form=quiz_form, quiz_data=quiz_data, quiz=quiz, answer_key=answer_key)

    # TODO Check return code

    # Remove the quiz objects
    if 'quiz' in request.session and 'quiz_data' in request.session and 'quiz_form' in request.session:
        del request.session['quiz']
        del request.session['quiz_data']
        del request.session['quiz_form']

    return HttpResponseRedirect(reverse(SERVICE_USER_HOME))
