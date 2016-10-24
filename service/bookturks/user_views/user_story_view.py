"""
User Story View
"""

from service.bookturks.Constants import USER_STORY_HOME_PAGE
from service.bookturks.decorators.Controller import controller
from service.bookturks.models import ControllerModel


@controller
def user_story_home_view(request):
    """
    User write a story home page.
    :param request:
    :return:
    """
    return ControllerModel(view=USER_STORY_HOME_PAGE, redirect=False)
