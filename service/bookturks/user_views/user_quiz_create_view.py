"""
User Quiz Views
"""

from dateutil.parser import parse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from service.bookturks.Constants import SERVICE_USER_QUIZ_INIT, SERVICE_USER_HOME, USER_QUIZ_INIT_PAGE, \
    USER_QUIZ_MAKER_PAGE, USER_QUIZ_VERIFIER_PAGE, SERVICE_USER_MYQUIZ_HOME, REQUEST, USER, \
    ALERT_MESSAGE, ALERT_TYPE, DANGER, SUCCESS
from service.bookturks.adapters import UserAdapter, QuizAdapter, QuizTagAdapter
from service.bookturks.alerts import init_alerts, set_alert_session
from service.bookturks.models.EventModel import EventModel
from service.bookturks.models.QuizCompleteModel import QuizCompleteModel
from service.bookturks.quiz.QuizTools import QuizTools
from service.bookturks.session_handler import session_insert_keys, session_remove_keys
from service.bookturks.user.UserProfileTools import UserProfileTools


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
        ALERT_TYPE: alert_type,
        # "quiz_tag_names": json.dumps(quiz_tag_names, ensure_ascii=False)
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
    start_date_time = request.POST.get('start_date_time')
    end_date_time = request.POST.get('end_date_time')
    attempts = request.POST.get('attempts')
    pass_percentage = request.POST.get('pass_percentage')
    tag_names = request.POST.get('quiz_tags')

    local = timezone.get_current_timezone()
    event_model = None
    # TODO: Remove this from here and put it in a function.
    if start_date_time and end_date_time:
        event_start_date_time = (local.localize(parse(start_date_time), is_dst=None)).astimezone(timezone.utc)
        event_end_date_time = (local.localize(parse(end_date_time), is_dst=None)).astimezone(timezone.utc)
        event_model = EventModel(start_time=event_start_date_time, end_time=event_end_date_time)

    request, alert_type, alert_message = init_alerts(request=request)

    # Initialize the adapters.
    user_adapter = UserAdapter()
    quiz_adapter = QuizAdapter()
    quiz_tag_adapter = QuizTagAdapter()

    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type
    }

    try:

        # Get the user model from the request.
        user = user_adapter.get_user_instance_from_django_user(request.user)

        if not user:
            raise ValueError("User not recognized")

        # quiz_name could be None if there were errors in creating the model
        # Check if quiz_id is not set after creating the id. (This will mostly be true as we already have this check in
        # the javascript)
        quiz = quiz_adapter.get_quiz_for_owner(user, quiz_name)
        if quiz:
            raise ValueError("Quiz already present")

        # Create the quiz model
        quiz = quiz_adapter.create_model(quiz_name=quiz_name, quiz_description=quiz_description,
                                         quiz_owner=user, start_time=event_start_date_time, end_time=event_end_date_time)

        quiz_complete_model = QuizCompleteModel(quiz_model=quiz,
                                                attempts=attempts,
                                                pass_percentage=pass_percentage,
                                                event_model=event_model,
                                                tags=list())

        # Create the tag names and put them into the quiz_complete_model
        tag_names_list = quiz_tag_adapter.split_and_verify_tag_names(tag_names)
        if tag_names_list:
            for tag_name in tag_names_list:
                quiz_complete_model.tags.append(tag_name)

    except ValueError as err:
        set_alert_session(session=request.session,
                          message=str(err),
                          alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    session_insert_keys(session=request.session, quiz_complete_model=quiz_complete_model)

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

    try:
        # Do not allow empty forms to be submitted
        if not quiz_data or not quiz_form:
            raise ValueError("Quiz data was not provided")

        # Parse the form to remove irrelevant data.
        # It will be better and cleaner to change the javascript so this will not be required
        quiz_form = quiz_tools.parse_form(quiz_form=quiz_form)

    except ValueError as err:
        set_alert_session(session=request.session,
                          message=str(err),
                          alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    # Add this form so that it can be displayed in the next page
    context = {
        'quiz_form': quiz_form,
    }
    # Save to session to pass to the next view
    quiz_complete_model = request.session.get('quiz_complete_model')
    quiz_complete_model.quiz_form = quiz_form
    quiz_complete_model.quiz_data = quiz_data
    session_insert_keys(request.session, quiz_complete_model=quiz_complete_model)

    return render(request, USER_QUIZ_VERIFIER_PAGE, context)


def user_quiz_create_view(request):
    """
    Creates the quiz and uploads to storage.
    :param request: User request
    :return: Redirects to dashboard on successful quiz creation.
    """
    quiz_tools = QuizTools()
    quiz_adapter = QuizAdapter()
    quiz_tag_adapter = QuizTagAdapter()

    answer_key = request.POST
    quiz_complete_model = request.session.get('quiz_complete_model')

    try:
        # Create serialized content to be uploaded to storage
        content = quiz_tools.create_content(quiz_complete_model=quiz_complete_model, answer_key=answer_key)

        # Create filename for file in storage
        filename = quiz_tools.create_filename(quiz=quiz_complete_model.quiz_model)

        # Upload file to storage and get the return code (file id)
        quiz_tools.upload_quiz(content=content, filename=filename)

    except ValueError as err:
        set_alert_session(session=request.session,
                          message=str(err),
                          alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))
    except Exception:
        # Remove the quiz objects so that new form can be generated without mixing up old data
        session_remove_keys(request.session, "quiz_complete_model")

        set_alert_session(session=request.session, message="An error occurred creating the quiz.", alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_QUIZ_INIT))

    # Same model treated as 2 different objects if constructed again from string.
    # This is executed twice when someone edits the quiz. Redirected from myquiz_info
    if not quiz_adapter.exists(quiz_complete_model.quiz_model.quiz_id):
        quiz_complete_model.quiz_model.save()

    # Save the quiz tags and links
    for tag_name in quiz_complete_model.tags:
        if not quiz_tag_adapter.exists(tag_name):
            quiz_tag_adapter.create_and_save_model(tag_name)
        quiz_tag_adapter.link_quiz(tag_name=tag_name, quiz_id=quiz_complete_model.quiz_model.quiz_id)

    # Save quiz in model of user profile
    UserProfileTools.save_my_quiz_profile(session=request.session, quiz_model=quiz_complete_model.quiz_model)

    # Save the profile
    user_profile_tools = UserProfileTools()
    future = user_profile_tools.save_profile(request.session)
    # Wait for asynchronous callback
    future.result()

    # Remove the quiz objects
    session_remove_keys(request.session, "quiz_complete_model")

    set_alert_session(session=request.session, message="The quiz has been successfully saved", alert_type=SUCCESS)
    return HttpResponseRedirect(reverse(SERVICE_USER_HOME))


def user_quiz_delete_view(request):
    """
    Deletes
    :param request:
    :return:
    """
    quiz_tools = QuizTools()
    user_adapter = UserAdapter()
    quiz_adapter = QuizAdapter()

    quiz_id = request.POST.get('quiz_id')
    quiz = quiz_adapter.exists(quiz_id)

    try:
        # Check whether user deleting this quiz is admin or owner or any other staff person
        if not request.user.is_staff and \
                not (user_adapter.get_user_instance_from_django_user(request.user) == quiz.quiz_owner):
            raise ValueError("You do not have the permission to delete this quiz. This action will be reported")
        if not quiz:
            raise ValueError("No such quiz.")

        # Unlink all tags from the quiz
        quiz_tools.unlink_all_tags_of_quiz(quiz)
        # Deletes from storage
        quiz_tools.delete_quiz_from_storage(quiz)
        # Deletes from database
        quiz_adapter.delete_model(quiz)
        # Deletes from the user profile
        UserProfileTools.remove_my_quiz_profile(session=request.session, quiz_model=quiz)

        # Save the profile
        user_profile_tools = UserProfileTools()
        future = user_profile_tools.save_profile(request.session)
        # Wait for asynchronous callback
        future.result()

    except ValueError as err:
        set_alert_session(session=request.session,
                          message=str(err),
                          alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_USER_MYQUIZ_HOME))

    set_alert_session(session=request.session, message="The quiz has been successfully deleted", alert_type=SUCCESS)
    return HttpResponseRedirect(reverse(SERVICE_USER_MYQUIZ_HOME))
