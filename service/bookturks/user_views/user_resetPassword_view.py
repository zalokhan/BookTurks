from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from sendgrid.helpers.mail import *

from service.bookturks.adapters.UserAdapter import UserAdapter
from service.bookturks.alerts import init_alerts, set_alert_session
from service.bookturks.Constants import DANGER, SUCCESS, RESET_PASSWORD_CONFIRM, SERVICE_MAIN_HOME

import sendgrid


def get_username_password_reset_view(request):
    username = request.POST.get('username')

    user_adapter = UserAdapter()
    if validate_email_address(username) is True:
        try:
            user = user_adapter.get_user_from_django(username)
        except Exception:
            set_alert_session(session=request.session,
                              message=str("The user does not exist."),
                              alert_type=DANGER)
            return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))
        content = craft_email(request, user)
        send_email(content, user.email)
        success_alert = "An email has been sent to " + user.email +\
                        ". Please check the inbox to reset the password."
        set_alert_session(session=request.session,
                          message=success_alert,
                          alert_type=SUCCESS)
    else:
        set_alert_session(session=request.session,
                          message=str("The email address is not valid."),
                          alert_type=DANGER)
    return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))


def get_password_confirmation(request, uidb64=None, token=None, *args, **kwargs):
    if request.method == 'GET':
        return render(request, RESET_PASSWORD_CONFIRM, {'uidb64': uidb64, 'token': token})

    # uidb64, token is for verification purpose
    new_password = request.POST.get('password')
    uidb64 = request.POST.get('uidb64')
    token = request.POST.get('token')
    user_adapter = UserAdapter()
    try:
        assert uidb64 is not None and token is not None
        uid = urlsafe_base64_decode(uidb64)
        user = user_adapter.get_user_from_django_pk(uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Changing password
        user_adapter.user_change_password(user, new_password)

        success_alert = 'Password has been reset.'
        set_alert_session(session=request.session, message=success_alert, alert_type=SUCCESS)
        return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))
    else:
        failure_alert = 'Password reset has not been unsuccessful.'
        set_alert_session(session=request.session, message=failure_alert, alert_type=DANGER)
        return HttpResponseRedirect(reverse(SERVICE_MAIN_HOME))


def craft_email(request, user):
    c = {
        'email': user.email,
        'domain': request.META['HTTP_HOST'],
        'site_name': 'www.bookturks.com',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
    }
    return c


def send_email(content, username):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    subject_template_name = 'service/password_reset_subject.txt'
    email_template_name = 'service/password_reset_email.html'
    subject = loader.render_to_string(subject_template_name, content)

    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    # Rendering the content and jsonify it
    content = loader.render_to_string(email_template_name, content)
    content = Content("text/plain", content)

    from_email = Email("support@bookturks.com")
    to_email = Email(username)

    # Sending email
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
