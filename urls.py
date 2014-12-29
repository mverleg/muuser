
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from muuser.views.login import login
from muuser.views.logout import logout
from muuser.views.register import register
from muuser.views.profile import profile
from muuser.views.reset import reset_request, reset_sent, reset_new, reset_complete
from muuser.views.subscribe import email_unsubscribe, email_subscribe
from muuser.views.profile_actions import profile_actions
from muuser.views.settings import settings
from muuser.views.password import password, password_done


pattern_list = (
	url(r'^$', lambda request: redirect(reverse('profile_actions')), name = 'profile'),
	url(r'^login/$', login, name = 'login'),
	url(r'^logout/$', logout, name = 'logout'),
	url(r'^register/$', register, name = 'register'),
	url(r'^actions/$', profile_actions, name = 'profile_actions'),
	url(r'^profile/$', profile, name = 'profile_info'),
	url(r'^settings/$', settings, name = 'profile_settings'),
	url(r'^password/$', password, name = 'profile_password'),
	url(r'^password/done/$', password_done, name = 'profile_password_done'),

	url(r'^reset/$', reset_request, name = 'password_reset'),
	url(r'^reset/sent/$', reset_sent, name = 'password_reset_sent'),
	url(r'^reset/new/(?P<uid>[0-9]+)/(?P<token>[a-zA-Z0-9]+)/$', reset_new, name = 'password_reset_new'),
	url(r'^reset/complete/$', reset_complete, name = 'password_reset_complete'),
	url(r'^unsubscribe/(?P<uid>[0-9]+)/(?P<token>[a-zA-Z0-9]+)/$', email_unsubscribe, name = 'email_unsubscribe'),
	url(r'^subscribe/$', email_subscribe, name = 'email_subscribe'),
)
urlpatterns = patterns('', *pattern_list)


