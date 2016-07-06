"""
User Home View
"""
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from service.bookturks.alerts import init_alerts
from service.bookturks.Constants import USER_HOME_PAGE, REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE, SERVICE_USER_SETUP
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

    user_adapter = UserAdapter()
    user_profile_tools = UserProfileTools()

    if 'user_profile_model' not in request.session:
        user_model = user_adapter.get_user_instance_from_request(request)
        if not user_model:
            return HttpResponseRedirect(reverse(SERVICE_USER_SETUP))
        user_profile_model = user_profile_tools.get_profile(user_model)
        request.session['user_profile_model'] = user_profile_model

    user_profile_tools = UserProfileTools()
    future = user_profile_tools.save_profile(request.session)
    # Wait for asynchronous callback
    future.result()

    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type,
        'UserProfileModel': request.session.get('user_profile_model')
    }

    return render(request, USER_HOME_PAGE, context)
