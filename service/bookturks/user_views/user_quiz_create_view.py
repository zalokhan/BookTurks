"""
User Quiz Views
"""
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.adapters.QuizAdapter import QuizAdapter
from service.bookturks.quiz.QuizMaker import quiz_form_data_parser, create_quiz_content, QuizMaker

from service.bookturks.alerts import init_alerts, set_alert_session
from service.bookturks.Constants import SERVICE_USER_QUIZ_INIT, SERVICE_USER_HOME, USER_QUIZ_INIT_PAGE, \
    USER_QUIZ_MAKER_PAGE, USER_QUIZ_VERIFIER_PAGE, \
    REQUEST, USER, \
    ALERT_MESSAGE, ALERT_TYPE, DANGER, SUCCESS


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
    user_adapter = UserAdapter()
    quiz_adapter = QuizAdapter()

    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type
    }

    if not quiz_id or not quiz_id.rstrip():
        set_alert_session(session=request.session, message="The quiz id cannot be empty.", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    if not quiz_adapter.exists(quiz_id):
        user = user_adapter.get_user_instance_from_request(request)

        if not user:
            set_alert_session(session=request.session, message="User not recognizes", alert_type=DANGER)
            return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

        quiz = quiz_adapter.create_model(quiz_id=quiz_id, quiz_name=quiz_name, quiz_description=quiz_description,
                                         quiz_owner=user)
        if not quiz:
            set_alert_session(session=request.session, message="Quiz ID already present", alert_type=DANGER)
            return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))
    else:
        set_alert_session(session=request.session, message="Quiz ID already present", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    set_alert_session(session=request.session, message=" ".join([quiz_id, "created successfully"]), alert_type=SUCCESS)
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
        set_alert_session(session=request.session, message="Quiz data was not provided", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    try:
        quiz_form = quiz_form_data_parser(form_data=quiz_form)
    except ValueError:
        set_alert_session(session=request.session, message="Empty quizzes cannot be submitted", alert_type=DANGER)
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
        if not quiz_form or not quiz_data or not quiz or not answer_key:
            raise ValueError("quiz_data or quiz_form or quiz is None")
        return_code = create_quiz_content(quiz_form=quiz_form, quiz_data=quiz_data, quiz=quiz, answer_key=answer_key)
    except:
        # Remove the quiz objects
        if 'quiz' in request.session and 'quiz_data' in request.session and 'quiz_form' in request.session:
            del request.session['quiz']
            del request.session['quiz_data']
            del request.session['quiz_form']
        set_alert_session(session=request.session, message="An error occurred creating the quiz.", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    if return_code:
        quiz.save()
    # Remove the quiz objects
    if 'quiz' in request.session and 'quiz_data' in request.session and 'quiz_form' in request.session:
        del request.session['quiz']
        del request.session['quiz_data']
        del request.session['quiz_form']

    set_alert_session(session=request.session, message="The quiz has been successfully created", alert_type=SUCCESS)
    return HttpResponseRedirect(reverse(SERVICE_USER_HOME))
