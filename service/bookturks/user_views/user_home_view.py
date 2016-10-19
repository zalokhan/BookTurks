"""
User Home View
"""

from service.bookturks.Constants import USER_HOME_PAGE, SERVICE_USER_SETUP, USER_PROFILE_MODEL
from service.bookturks.adapters import UserAdapter
from service.bookturks.decorators.Controller import controller
from service.bookturks.models import ControllerModel
from service.bookturks.utils.UserProfileTools import UserProfileTools


@controller
def user_home_main_view(request):
    """
    User Home page. Lands on the dashboard page
    If not authenticated redirects back to main page
    :param request:
    :return: Renders user_home page (dashboard)
    """
    user_adapter = UserAdapter()
    user_profile_tools = UserProfileTools()

    if USER_PROFILE_MODEL not in request.session:
        user_model = user_adapter.get_user_instance_from_django_user(request.user)
        if not user_model:
            return ControllerModel(view=SERVICE_USER_SETUP, redirect=True)
        request.session[USER_PROFILE_MODEL] = user_profile_tools.get_profile(user_model)

    context = {
        USER_PROFILE_MODEL: request.session.get(USER_PROFILE_MODEL)
    }

    return ControllerModel(view=USER_HOME_PAGE, redirect=False, context=context)
