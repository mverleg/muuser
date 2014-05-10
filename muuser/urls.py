
from django.conf.urls import patterns, url
from views.login import login
from views.logout import logout
from views.register import register
from views.profile import profile, profile_submit, profile_password, profile_password_done
from views.reset import reset_request, reset_sent, reset_new, reset_complete
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


urlpatterns = patterns('',
	url(r'^$', lambda request: redirect(reverse('profile'))),
	url(r'^login/$', login, name = 'login'),
	url(r'^logout/$', logout, name = 'logout'),
	url(r'^register/$', register, name = 'register'),
	url(r'^profile/$', profile, name = 'profile'),
	url(r'^profile/submit/$', profile_submit, name = 'profile_submit'),
	url(r'^password/$', profile_password, name = 'profile_password'),
	url(r'^password/done/$', profile_password_done, name = 'profile_password_done'),
	
	url(r'^reset/$', reset_request, name = 'password_reset'),
	url(r'^reset/sent/$', reset_sent, name = 'password_reset_sent'),
	url(r'^reset/new/(?P<uid>[0-9]+)/(?P<token>[a-zA-Z0-9]+)/$', reset_new, name = 'password_reset_new'),
	url(r'^reset/complete/$', reset_complete, name = 'password_reset_complete'),
)


#reset_complete.html  reset_done.html   reset_form.html
#reset_confirm.html	 reset_email.html
