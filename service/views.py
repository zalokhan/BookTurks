"""
Views
"""
from django.contrib.auth.decorators import login_required

from service.bookturks.Constants import SERVICE_MAIN_HOME
from service.bookturks.auth.authentication import login_check_view, logout_view, user_setup_view
from service.bookturks.main_home_view import main_home_view
from service.bookturks.register_view import register_view, register_check_view
from service.bookturks.user_views.user_home_view import user_home_main_view
from service.bookturks.user_views.user_myquiz_view import user_myquiz_home_view, user_myquiz_info_view
from service.bookturks.user_views.user_quiz_create_view import user_quiz_init_view, user_quiz_maker_view, \
    user_quiz_verifier_view, user_quiz_create_view, user_quiz_delete_view
from service.bookturks.user_views.user_quizarena_view import user_quizarena_home_view, user_quizarena_solve_view, \
    user_quizarena_result_view
from service.bookturks.user_views.user_story_view import user_story_home_view


def main_home(request):
    """
    Main Home Page
    Website landing page
    :param request: User request
    :return: Renders a page
    """
    return main_home_view(request)


def login(request):
    """
    Login Check
    Validates login values
    :param request: User request
    :return: Renders a page
    """
    return login_check_view(request)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_setup(request):
    """
    User profile setup
    :param request:
    :return:
    """
    return user_setup_view(request)


def logout(request):
    """
    Logout
    Logs out the user
    :param request: User request
    :return: Renders a page
    """
    return logout_view(request)


def register(request):
    """
    Register Page
    Register new account landing page
    :param request: User request
    :return: Renders a page
    """
    return register_view(request)


def register_check(request):
    """
    Register Check
    Validates registration values
    :param request: User request
    :return: Renders a page
    """
    return register_check_view(request)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_home(request):
    """
    User Home page
    User Dashboard and home landing page
    :param request: User request
    :return: Renders a page
    """
    return user_home_main_view(request)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_quiz_init(request):
    """
    User Quiz Name verifier and initialization
    :param request: User request
    :return: Renders quiz name form
    """
    return user_quiz_init_view(request)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_quiz_maker(request):
    """
    User Quiz Maker page
    :param request: User request
    :return:  Renders a page
    """
    return user_quiz_maker_view(request)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_quiz_verifier(request):
    """
    User Quiz Verifier page and answer key generator
    :param request: User request
    :return:  Renders a page
    """
    return user_quiz_verifier_view(request)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_quiz_create(request):
    """
    Creates the quiz and uploads to the storage
    :param request: User request
    :return: Redirects to dashboard
    """
    return user_quiz_create_view(request)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_quiz_delete(request):
    """
    Deletes quiz from storage and database
    :param request: User request
    :return: Redirects to User quizzes
    """
    return user_quiz_delete_view(request)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_myquiz_home(request):
    """
    Landing page for user's quizzes
    :param request: User request
    :return: Redirects to quiz home
    """
    return user_myquiz_home_view(request)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_myquiz_info(request, quiz_id):
    """
    One page for all quiz id related tasks
    :param request:
    :param quiz_id:
    :return:
    """
    return user_myquiz_info_view(request, quiz_id)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_quizarena_home(request):
    """
    Attempt quizzes here. Displays a list of quizzes which you can attempt
    :param request:
    :return:
    """
    return user_quizarena_home_view(request)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_quizarena_solve(request, quiz_id):
    """
    Attempt quizzes here
    :param request:
    :param quiz_id:
    :return:
    """
    return user_quizarena_solve_view(request, quiz_id)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_quizarena_result(request):
    """
    Result of your quiz attempt
    :param request:
    :return:
    """
    return user_quizarena_result_view(request)


@login_required(login_url=SERVICE_MAIN_HOME)
def user_story_home(request):
    """
    Home page of write a story.
    :param request:
    :return:
    """
    return user_story_home_view(request)
