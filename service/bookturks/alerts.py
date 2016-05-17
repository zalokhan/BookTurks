"""
Check and refresh alerts
"""

from service.bookturks.Constants import ALERT_TYPE, ALERT_MESSAGE


def init_alerts(request):
    """
    Initializes alerts
    :param request: User request
    :return: returns alert message and alert type
    """
    # Checks if alert message is required to be displayed on the top
    # Alert type is the severity level of the alert box: success(green) or danger(red)
    alert_message = request.session.get(ALERT_MESSAGE)
    alert_type = request.session.get(ALERT_TYPE)

    # Remove the alerts from the request to prevent repetition of alerts on reload of the page
    if ALERT_MESSAGE in request.session:
        del request.session[ALERT_MESSAGE]
        del request.session[ALERT_TYPE]

    return request, alert_type, alert_message
