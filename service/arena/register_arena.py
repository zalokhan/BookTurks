from django.http import HttpResponseRedirect
from django.http import Http404

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from service.models import User as UserModel

"""
Register
Returns page when user clicks the register button
or redirected from invalid registration
"""


def register_arena(request):
    alert_message = request.session.get('alert_message')
    alert_type = request.session.get('alert_type')
    if 'alert_message' in request.session:
        del request.session['alert_message']
        del request.session['alert_type']
    return render(request, 'service/register.html', {'alert_message': alert_message, 'alert_type': alert_type})


"""
Register validation
Validates the input by the user and checks for duplicates or invalid inputs.
"""


def register_check_arena(request):
    username = request.POST['username']
    user_first_name = request.POST['user_first_name']
    user_last_name = request.POST['user_last_name']
    user_phone = request.POST['user_phone']
    user_dob = request.POST['user_dob']
    password = request.POST['password']
    repassword = request.POST['repassword']

    if username is None or \
                    user_first_name is None or \
                    user_last_name is None or \
                    user_phone is None or \
                    user_dob is None or \
                    password is None or \
                    password != repassword:
        message = "The password should be same in both the fields"
        alert_type = "danger"
        request.session['alert_message'] = message
        request.session['alert_type'] = alert_type
        return HttpResponseRedirect(reverse('service:register'))

    try:
        get_object_or_404(UserModel, username=username)
    except Http404:
        pass
    else:
        message = "User ID already present"
        alert_type = "danger"
        request.session['alert_message'] = message
        request.session['alert_type'] = alert_type
        return HttpResponseRedirect(reverse('service:register'))

    auth_user = User.objects.create_user(username, username, password)
    auth_user.first_name = user_first_name
    auth_user.last_name = user_last_name

    user = UserModel(username=username,
                     user_first_name=user_first_name,
                     user_last_name=user_last_name,
                     user_phone=user_phone,
                     user_dob=user_dob)
    user.save()
    message = " ".join([user_first_name, user_last_name, "registered successfully"])
    alert_type = "success"
    request.session['alert_message'] = message
    request.session['alert_type'] = alert_type
    return HttpResponseRedirect(reverse('service:main_home'))
