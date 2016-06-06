"""
User Home View
"""
from django.shortcuts import render

from service.bookturks.alerts import init_alerts, set_alert_session
from service.bookturks.Constants import USER_HOME_PAGE, REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE, \
    DANGER
from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.user.UserProfileTools import UserProfileTools


def user_home_main_view(request):
    """
    User Home page. Lands on the dashboard page
    If not authenticated redirects back to main page
    :param request:
    :return: Renders user_home page (dashboard)
    """
    request, alert_type, alert_message = init_alerts(request=request)
    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type
    }
    user_adapter = UserAdapter()
    user_profile_tools = UserProfileTools()

    user_model = user_adapter.get_user_instance_from_request(request)

    user_profile_model = user_profile_tools.get_profile(user_model)
    request.session['user_profile_model'] = user_profile_model

    return render(request, USER_HOME_PAGE, context)
