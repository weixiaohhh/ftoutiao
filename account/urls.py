# coding:utf-8
from django.conf.urls import url
from django.contrib.auth.views import login, logout, logout_then_login,\
    password_change, password_change_done, password_reset, password_reset_done,\
    password_reset_confirm, password_reset_complete
from . import views
urlpatterns = [
    # previous login view
    # url(r'^login/$', views.user_login, name='login'),
    # login / logout urls
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    url(r'^$', views.dashboard, name='dashboard'),

    # password
    url(r'^password-change/$', password_change,
        {'template_name': 'registration/password_change.html'},
        name='password_change'),
    url(r'^password-change/done/$', password_change_done,
        {'template_name': 'registration/password_c_d.html'},
        name='password_change_done'),

    # reset
    url(r'^password-reset/$',
        password_reset,
        {'template_name': 'registration/password_rs_form.html'},
        name='password_reset'),
    url(r'^password-reset/done/$',
        password_reset_done,
        {'template_name': 'registration/password_rs_done.html'},
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        password_reset_confirm,
        {'template_name': 'registration/password_rs_confirm.html'},
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        password_reset_complete,
        {'template_name': 'registration/password_rs_complete.html'},
        name='password_reset_complete'),

    # register
    url(r'^register/$', views.register, name='register'),

    # edit
    url(r'^profile/$', views.profile, name='profile'),
]
