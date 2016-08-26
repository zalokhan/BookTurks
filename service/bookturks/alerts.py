"""
Check and refresh alerts
"""

from service.bookturks.Constants import ALERT_TYPE, ALERT_MESSAGE
from service.bookturks.session_handler import session_insert_keys, session_remove_keys


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
    session_remove_keys(request.session, ALERT_MESSAGE, ALERT_TYPE)

    return request, alert_type, alert_message


def set_alert_session(session, message, alert_type):
    """
    set alert session and message and save.
    :param session:
    :param message:
    :param alert_type:
    :return:
    """
    session_insert_keys(session, alert_message=message, alert_type=alert_type)
