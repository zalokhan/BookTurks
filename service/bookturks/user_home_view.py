"""
User account pages
"""
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from Constants import SERVICE_MAIN_HOME, USER_HOME_PAGE


def user_home_main_arena(request):
    """
    User Home page. Lands on the dashboard page
    If not authenticated redirects back to main page
    :param request:
    :return: Renders user_home page (dashboard)
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))

    # debug line
    print request.user

    return render(request, USER_HOME_PAGE)


def user_quiz_arena(request):
    """
    Quiz landing page for user
    :param request: User request
    :return: Renders quiz page
    """

    return render(request, "service/user_quiz.html")
