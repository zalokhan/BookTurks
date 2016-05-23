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

    # User Quiz pages
    # Quiz Name Verifier
    url(r'^quiz/init/$', views.user_quiz_init, name='user_quiz_init'),
    # Quiz Maker
    url(r'^quiz/maker/$', views.user_quiz_maker, name='user_quiz_maker'),
    # Quiz Answer
    url(r'^quiz/verifier/$', views.user_quiz_verifier, name='user_quiz_verifier'),
    # Quiz Create
    url(r'^quiz/create/$', views.user_quiz_create, name='user_quiz_create'),

    # My quizzes
    url(r'^myquiz/home/$', views.user_myquiz_home, name='user_myquiz_home'),
    # Quiz editting page
    url(r'^myquiz/home/id/(?P<quiz_id>\w+)/$', views.user_myquiz_info, name='user_myquiz_info'),

    # Quiz Arena home page
    url(r'^quizarena/home/$', views.user_quizarena_home, name='user_quizarena_home'),

]
