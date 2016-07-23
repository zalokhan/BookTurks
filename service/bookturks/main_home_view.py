from django.shortcuts import render

from service.bookturks.alerts import init_alerts

from service.bookturks.Constants import ALERT_MESSAGE, ALERT_TYPE, MAIN_HOME_PAGE, USER, REQUEST


def main_home_view(request):
    """
    Main home page
    Sends alerts if registration successful or login failure
    :param request: user request
    :return: renders a page with context
    """
    # Clearing and displaying any alerts passed
    request, alert_type, alert_message = init_alerts(request=request)

    # Creating context
    context = {
        REQUEST: request,
        USER: request.user,
        ALERT_MESSAGE: alert_message,
        ALERT_TYPE: alert_type
    }

    return render(request, MAIN_HOME_PAGE, context)
