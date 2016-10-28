"""
Arena to attempt quizzes
"""

from service.bookturks.Constants import DANGER, \
    USER_QUIZARENA_HOME_PAGE, SERVICE_USER_QUIZARENA_HOME, USER_QUIZARENA_SOLVE_PAGE, USER_QUIZARENA_RESULT_PAGE, \
    USER_PROFILE_MODEL
from service.bookturks.adapters import QuizAdapter, UserAdapter
from service.bookturks.alerts import set_alert_session
from service.bookturks.decorators.Controller import controller
from service.bookturks.models import ControllerModel
from service.bookturks.storage_handlers import QuizStorageHandler, UserProfileStorageHandler
from service.bookturks.utils import QuizChecker, QuizTools, UserProfileTools


@controller
def user_quizarena_home_view(request):
    """
    Home page for the quiz arena
    :param request:
    :return:
    """
    quiz_adapter = QuizAdapter()

    # Gets only the quizzes which have valid event windows.
    quiz_list = quiz_adapter.get_valid_quizzes()
    context = {'quiz_list': quiz_list}

    return ControllerModel(view=USER_QUIZARENA_HOME_PAGE, redirect=False, context=context)


@controller
def user_quizarena_solve_view(request, quiz_id):
    """
    Attempt the quiz here. Setup for the player to attempt.
    Disallow repeated attempts.
    :param request:
    :param quiz_id:
    :return:
    """
    quiz_adapter = QuizAdapter()
    quiz_tools = QuizTools()
    quiz_storage_handler = QuizStorageHandler()

    quiz = quiz_adapter.exists(quiz_id)
    try:
        if not quiz:
            raise ValueError("No such quiz present")
        quiz_complete_model = quiz_storage_handler.download_quiz_content(quiz_model=quiz)
        if not quiz_complete_model:
            raise ValueError("This quiz is unavailable")

        quiz_tools.check_quiz_eligibility((request.session.get(USER_PROFILE_MODEL)), quiz_complete_model, quiz_id)

    except ValueError as err:
        set_alert_session(session=request.session,
                          message=str(err),
                          alert_type=DANGER)
        return ControllerModel(view=SERVICE_USER_QUIZARENA_HOME, redirect=True)
    context = {'quiz_form': quiz_complete_model.quiz_form}

    request.session['quiz'] = quiz_complete_model.quiz_model

    return ControllerModel(view=USER_QUIZARENA_SOLVE_PAGE, redirect=False, context=context)


@controller
def user_quizarena_result_view(request):
    """
    Result of the quiz attempt
    :param request:
    :return:
    """
    quiz = request.session.get('quiz')

    user_adapter = UserAdapter()
    quiz_storage_handler = QuizStorageHandler()
    user_profile_storage_handler = UserProfileStorageHandler()
    quiz_checker = QuizChecker()
    # Get the user model from the request.
    user = user_adapter.get_user_instance_from_django_user(request.user)

    try:
        if not quiz or not user:
            raise ValueError("Invalid quiz attempt.")

        content = quiz_storage_handler.download_quiz_content(quiz_model=quiz)

        if not content:
            raise ValueError("This quiz is unavailable")

        answer_key = content.answer_key
        user_answer_key = dict(request.POST)

        quiz_result_model = quiz_checker.get_quiz_result(quiz_model=quiz, answer_key=answer_key,
                                                         user_answer_key=user_answer_key)
    except ValueError as err:
        set_alert_session(session=request.session,
                          message=str(err),
                          alert_type=DANGER)
        return ControllerModel(view=SERVICE_USER_QUIZARENA_HOME, redirect=True)

    # Save result in model
    UserProfileTools.save_attempted_quiz_profile(session=request.session, quiz_result_model=quiz_result_model)
    # Save the profile
    future = user_profile_storage_handler.save_profile(request.session)

    context = {'result': quiz_result_model}

    # Clearing the session
    del request.session['quiz']

    # Wait for asynchronous callback
    future.result()
    return ControllerModel(view=USER_QUIZARENA_RESULT_PAGE, redirect=False, context=context)
