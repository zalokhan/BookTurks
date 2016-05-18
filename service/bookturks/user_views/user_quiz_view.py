"""
User Quiz Views
"""
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from service.models import Quiz

from service.bookturks.alerts import init_alerts
from service.bookturks.Constants import SERVICE_USER_QUIZ_INIT, SERVICE_USER_HOME, USER_QUIZ_INIT_PAGE, \
    USER_QUIZ_MAKER_PAGE, USER_QUIZ_VERIFIER_PAGE, \
    REQUEST, USER, \
    ALERT_MESSAGE, ALERT_TYPE, DANGER, SUCCESS
from service.bookturks.quiz.QuizMaker import quiz_form_data_parser, create_quiz_content


def user_quiz_init_view(request):
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


def user_quiz_maker_view(request):
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

    if not quiz_id or not quiz_id.rstrip():
        message = "The quiz id cannot be empty."
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    try:
        get_object_or_404(Quiz, quiz_id=quiz_id)
    except Http404:
        # Quiz was not found so creating new quiz object for user
        quiz = Quiz(
            quiz_id=quiz_id,
            quiz_name=quiz_name,
            quiz_description=quiz_description,
            quiz_owner=request.user)

    else:
        message = "Quiz ID already present"
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    message = " ".join([quiz_id, "created successfully"])
    alert_type = SUCCESS
    request.session[ALERT_MESSAGE] = message
    request.session[ALERT_TYPE] = alert_type
    request.session['quiz'] = quiz

    return render(request, USER_QUIZ_MAKER_PAGE, context)


def user_quiz_verifier_view(request):
    """
    Verifies the form for errors
    Asks the user to prepare the answer key
    :param request: User request
    :return: Message depending on success or failure of quiz creation.
    """
    request, alert_type, alert_message = init_alerts(request=request)
    quiz_form = request.POST.get('quiz_form')
    quiz_data = request.POST.get('quiz_data')
    if not quiz_data or not quiz_form:
        message = "Quiz data was not provided"
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    try:
        quiz_form = quiz_form_data_parser(form_data=quiz_form)
    except ValueError:
        message = "Empty quizzes cannot be submitted"
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    context = {
        'quiz_form': quiz_form,
    }
    request.session['quiz_form'] = quiz_form
    request.session['quiz_data'] = quiz_data

    return render(request, USER_QUIZ_VERIFIER_PAGE, context)


def user_quiz_create_view(request):
    """
    Creates the quiz and uploads to storage.
    :param request: User request
    :return: Redirects to dashboard on successful quiz creation.
    """
    answer_key = request.POST

    quiz_form = request.session.get('quiz_form')
    quiz_data = request.session.get('quiz_data')
    quiz = request.session.get('quiz')

    try:
        return_code = create_quiz_content(quiz_form=quiz_form, quiz_data=quiz_data, quiz=quiz, answer_key=answer_key)
    except:
        # Remove the quiz objects
        if 'quiz' in request.session and 'quiz_data' in request.session and 'quiz_form' in request.session:
            del request.session['quiz']
            del request.session['quiz_data']
            del request.session['quiz_form']
        message = "An error occurred creating the quiz."
        alert_type = DANGER
        request.session[ALERT_MESSAGE] = message
        request.session[ALERT_TYPE] = alert_type
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    if return_code:
        quiz.save()
    # Remove the quiz objects
    if 'quiz' in request.session and 'quiz_data' in request.session and 'quiz_form' in request.session:
        del request.session['quiz']
        del request.session['quiz_data']
        del request.session['quiz_form']

    message = "The quiz has been successfully created"
    alert_type = SUCCESS
    request.session[ALERT_MESSAGE] = message
    request.session[ALERT_TYPE] = alert_type
    return HttpResponseRedirect(reverse(SERVICE_USER_HOME))
