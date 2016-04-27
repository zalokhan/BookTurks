from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout

"""
Main home page
Sends alerts if registration successful or login failure
"""


def main_home_arena(request):
    alert_message = request.session.get('alert_message')
    alert_type = request.session.get('alert_type')
    if 'alert_message' in request.session:
        del request.session['alert_message']
        del request.session['alert_type']
    context = {
        'request': request,
        'user': request.user,
        'alert_message': alert_message,
        'alert_type': alert_type
    }

    return render(request, 'service/main_home_page.html', context)


"""
Checks login authentication result
Gives failure alert if unsuccessful
"""


def login_check_arena(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('service:user_home'))
        else:
            message = "This account has been disabled. Contact the admin."
            alert_type = "danger"
            request.session['alert_message'] = message
            request.session['alert_type'] = alert_type
            return HttpResponseRedirect(reverse('service:main_home'))
    else:
        # the authentication system was unable to verify the username and password
        message = "The username or password were incorrect."
        alert_type = "danger"
        request.session['alert_message'] = message
        request.session['alert_type'] = alert_type
        return HttpResponseRedirect(reverse('service:main_home', ))


"""
Logs out user
"""


def logout_arena(request):
    logout(request)
    return HttpResponseRedirect(reverse('service:main_home', ))
