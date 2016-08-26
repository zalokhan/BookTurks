from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from service.bookturks.alerts import set_alert_session
from service.bookturks.Constants import USERNAME, PASSWORD, DANGER, SERVICE_MAIN_HOME, SERVICE_USER_HOME, \
    SERVICE_USER_SETUP
from service.bookturks.adapters.UserAdapter import UserAdapter


def login_check_view(request):
    """
    Checks login authentication result and gives failure alert if unsuccessful
    :param request: user request
    :return: renders a page with context
    """

    username = request.POST.get(USERNAME)
    password = request.POST.get(PASSWORD)

    # Authenticate the user with the provided username and password.
    # Django authentication is used here.
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            # Authentication successful
            auth_login(request, user)
            return HttpResponseRedirect(reverse(SERVICE_USER_SETUP))

        else:
            # Authentication failure as user was disabled.
            # Creating respective alerts.
            set_alert_session(session=request.session, message="This account has been disabled. Contact the admin.",
                              alert_type=DANGER)
            return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))

    else:
        # Authentication failure
        # the authentication system was unable to verify the username and password
        set_alert_session(session=request.session, message="The username or password were incorrect.",
                          alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))


def user_setup_view(request):
    """
    Sets up the user profile and user models
    :param request:
    :return:
    """
    user_adapter = UserAdapter()

    # User Exists and nothing else required
    if user_adapter.exists(request.user):
        return HttpResponseRedirect(reverse(SERVICE_USER_HOME))

    # User does not exist but has email field in social authentication
    elif request.user.email and str(request.user.email).strip():
        # Creating username from email address
        username = "".join([str(request.user.pk), request.user.email])
        # username exists
        if user_adapter.exists(username):
            return HttpResponseRedirect(reverse(SERVICE_USER_HOME))
        # Create user
        else:
            if user_adapter.create_and_save_model(username=username, first_name=request.user.first_name,
                                                  last_name=request.user.last_name):
                return HttpResponseRedirect(reverse(SERVICE_USER_HOME))
            # This condition should never be encountered
            else:
                set_alert_session(session=request.session, message="Trouble signing in. Contact the support for help !",
                                  alert_type=DANGER)
                return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))

    # User not present and no email field (facebook) so creating username from username and pk
    else:
        # Creating username from pk and username in auth
        username = "".join([str(request.user.pk), request.user.username, "@bookturks.com"])
        if user_adapter.exists(username):
            return HttpResponseRedirect(reverse(SERVICE_USER_HOME))
        else:
            if user_adapter.create_and_save_model(username=username, first_name=request.user.first_name,
                                                  last_name=request.user.last_name):
                return HttpResponseRedirect(reverse(SERVICE_USER_HOME))
            else:
                set_alert_session(session=request.session, message="Trouble signing in. Contact the support for help !",
                                  alert_type=DANGER)
                return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))


def logout_view(request):
    """
    Logs out user
    :param request: user request
    :return: renders a page with context
    """
    logout(request)
    return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))
