"""
User Quiz Views
"""
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.adapters.QuizAdapter import QuizAdapter
from service.bookturks.quiz.QuizTools import QuizTools

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
    # Get the post variables from the quiz init view.
    quiz_name = request.POST.get('quiz_name')
    quiz_description = request.POST.get('quiz_description')

    request, alert_type, alert_message = init_alerts(request=request)

    # Initialize the adapters.
    user_adapter = UserAdapter()
    quiz_adapter = QuizAdapter()
    quiz_tools = QuizTools()

    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type
    }
    # Get the user model from the request.
    user = user_adapter.get_user_instance_from_request(request)

    quiz_id = quiz_tools.get_quiz_id(username=user.username, quiz_name=quiz_name)

    # Check if quiz_id is not set. (This will mostly be true as we already have this check in the javascript)
    if not quiz_id or not quiz_id.rstrip():
        set_alert_session(session=request.session,
                          message="The quiz Name can contain ony alphanumeric characters, spaces, "
                                  "'-', '?' and '_'",
                          alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    # Check if the quiz_id is already used before.
    if not quiz_adapter.exists(quiz_id):
        # If quiz id is original, check if user is not None
        if not user:
            set_alert_session(session=request.session, message="User not recognized", alert_type=DANGER)
            return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

        # Create the quiz model
        quiz = quiz_adapter.create_model(quiz_id=quiz_id, quiz_name=quiz_name, quiz_description=quiz_description,
                                         quiz_owner=user)
        # This could be None if there were errors in creating the model
        if not quiz:
            set_alert_session(session=request.session, message="Quiz ID already present", alert_type=DANGER)
            return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))
    # Quiz ID is duplicate
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
    quiz_tools = QuizTools()

    # Quiz form is the HTML form which can be displayed and submitted by a user
    quiz_form = request.POST.get('quiz_form')
    # Quiz data is the template created by the form builder. This can be editted
    quiz_data = request.POST.get('quiz_data')
    # Do not allow empty forms to be submitted
    if not quiz_data or not quiz_form:
        set_alert_session(session=request.session, message="Quiz data was not provided", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    try:
        # Parse the form to remove irrelevant data.
        # It will be better and cleaner to change the javascript so this will not be required
        quiz_form = quiz_tools.parse_form(quiz_form=quiz_form)
    except ValueError:
        set_alert_session(session=request.session, message="Empty quizzes cannot be submitted", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    # Add this form so that it can be displayed in the next page
    context = {
        'quiz_form': quiz_form,
    }
    # Save to session to pass to the next view
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

    # Quiz Form is the HTML form which can be displayed as quiz and submitted
    quiz_form = request.session.get('quiz_form')
    # Quiz Data is the editable form which needs to be rendered to obtain the HTML form
    quiz_data = request.session.get('quiz_data')
    quiz = request.session.get('quiz')

    quiz_tools = QuizTools()
    try:
        if not quiz_form or not quiz_data or not quiz or not answer_key:
            raise ValueError("quiz_data or quiz_form or quiz is None")
        print "test-2"
        # Create a JSON content to be uploaded to storage
        content = quiz_tools.create_content(quiz_form=quiz_form, quiz_data=quiz_data, quiz_model=quiz,
                                            answer_key=answer_key)
        print "test-1"
        # Create filename for file in storage
        filename = quiz_tools.create_filename(quiz=quiz)
        # Upload file to storage and get the return code (file id)
        print "test1"
        return_code = quiz_tools.upload_quiz(content=content, filename=filename)
        print "test2"
    except Exception, err:
        print (err)
        # Remove the quiz objects so that new form can be generated without mixing up old data
        if 'quiz' in request.session and 'quiz_data' in request.session and 'quiz_form' in request.session:
            del request.session['quiz']
            del request.session['quiz_data']
            del request.session['quiz_form']
        set_alert_session(session=request.session, message="An error occurred creating the quiz.", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    # If return code was not None, save quiz in database
    if return_code:
        quiz.save()
    # Remove the quiz objects
    if 'quiz' in request.session and 'quiz_data' in request.session and 'quiz_form' in request.session:
        del request.session['quiz']
        del request.session['quiz_data']
        del request.session['quiz_form']

    set_alert_session(session=request.session, message="The quiz has been successfully saved", alert_type=SUCCESS)
    return HttpResponseRedirect(reverse(SERVICE_USER_HOME))
