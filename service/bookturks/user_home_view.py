from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

"""
User Home page
Lands on the dashboard page
If not authenticated redirects back to main page
"""


def user_home_main_arena(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('service:main_home'))
    return render(request, 'service/user_home.html')
