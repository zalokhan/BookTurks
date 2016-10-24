from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from service.bookturks.Constants import REQUEST, USER, ALERT_MESSAGE, ALERT_TYPE
from service.bookturks.alerts import init_alerts
from service.bookturks.exceptions import NotImplementedException


def controller(controller_func):
    """
    Decorator for controllers
    :param controller_func:
    :return:
    """

    def controller_wrapper(*args, **kwargs):
        """
        Wrapper function
        :param kwargs:
        :return:
        """
        if kwargs:
            raise NotImplementedException("Keywords arguments not allowed. Only args.")
        request = args[0]
        request, alert_type, alert_message = init_alerts(request=request)
        result = controller_func(*args)

        if result.redirect:
            return HttpResponseRedirect(reverse(result.view))

        result.context[REQUEST] = request
        result.context[USER] = request.user
        result.context[ALERT_MESSAGE] = alert_message
        result.context[ALERT_TYPE] = alert_type

        return render(request, result.view, result.context)

    return controller_wrapper
