from service.bookturks.Constants import MAIN_HOME_PAGE
from service.bookturks.decorators.Controller import controller
from service.bookturks.models import ControllerModel


@controller
def main_home_view(request):
    """
    Main home page
    Sends alerts if registration successful or login failure
    :param request: user request
    :return: renders a page with context
    """
    return ControllerModel(view=MAIN_HOME_PAGE, redirect=False)
