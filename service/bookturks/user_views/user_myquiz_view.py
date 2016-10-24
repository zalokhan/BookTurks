"""
My quizzes page
"""

from service.bookturks.Constants import DANGER, \
    USER_MYQUIZ_HOME_PAGE, USER_MYQUIZ_INFO_PAGE, SERVICE_USER_MYQUIZ_HOME, SERVICE_USER_HOME
from service.bookturks.adapters import QuizAdapter, UserAdapter
from service.bookturks.alerts import set_alert_session
from service.bookturks.decorators.Controller import controller
from service.bookturks.models import ControllerModel
from service.bookturks.storage_handlers import QuizStorageHandler


@controller
def user_myquiz_home_view(request):
    """
    My quizzes home page
    :param request: User request
    :return: Renders page
    """
    user_adapter = UserAdapter()
    quiz_adapter = QuizAdapter()

    user = user_adapter.get_user_instance_from_django_user(request.user)

    quiz_list = quiz_adapter.get_models_for_owner(user_model=user)
    context = {'quiz_list': quiz_list}

    return ControllerModel(view=USER_MYQUIZ_HOME_PAGE, redirect=False, context=context)


@controller
def user_myquiz_info_view(request, quiz_id):
    """
    Quiz related tasks
    :param request:
    :param quiz_id:
    :return:
    """
    user_adapter = UserAdapter()
    quiz_adapter = QuizAdapter()
    quiz_storage_handler = QuizStorageHandler()

    try:
        user = user_adapter.get_user_instance_from_django_user(request.user)
        quiz = quiz_adapter.exists(quiz_id)
        if not quiz or not user:
            raise ValueError("No such quiz exists")

        # Check if this user is the owner of this quiz
        if user != quiz.quiz_owner:
            raise ValueError("You do not own this quiz. You are not allowed to edit this")

    except ValueError as err:
        set_alert_session(session=request.session,
                          message=str(err),
                          alert_type=DANGER)
        return ControllerModel(view=SERVICE_USER_HOME, redirect=True)

    # Different try block because redirection is different.
    try:
        # Downloading the content from storage.
        content = quiz_storage_handler.download_quiz_content(quiz_model=quiz)
        if not content:
            raise ValueError("This quiz is unavailable")

    except ValueError as err:
        set_alert_session(session=request.session,
                          message=str(err),
                          alert_type=DANGER)
        return ControllerModel(view=SERVICE_USER_MYQUIZ_HOME, redirect=True)

    # Passing these session objects as this page submits the result to user_quiz_verifier view which checks for them.
    request.session['quiz_complete_model'] = content

    context = {'quiz_data': content.quiz_data}
    return ControllerModel(view=USER_MYQUIZ_INFO_PAGE, redirect=False, context=context)
