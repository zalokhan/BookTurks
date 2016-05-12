from django.conf.urls import url

from . import views

app_name = 'service'
urlpatterns = [

    # Home page
    url(r'^$', views.main_home, name='main_home'),
    # Login authentication
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    # Register new user
    url(r'^register/$', views.register, name='register'),
    # Register successful
    url(r'^register/check/$', views.register_check, name='register_check'),
    # User Home page
    url(r'^home/$', views.user_home, name='user_home'),
    # User Quiz page
    url(r'^quiz/$', views.user_quiz, name='user_quiz'),
]
