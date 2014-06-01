
from django.contrib.auth.hashers import get_hasher
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.core.mail import send_mail
from settings import SITE_URL
from re import sub


'''
	create a reset token (by rehashing the user's password
	and filtering / stripping it a little)
'''
def reset_token(user):
	passwd = user.password
	hasher = get_hasher()
	token = hasher.encode(passwd, 'reset')
	token = sub(r'[^a-zA-Z0-9]+', '', token.split('$')[-1])
	return token[-20:]

'''
	send password reset link
'''
def send_reset_link(request, user, domain, from_email = None):
	if not user.has_usable_password():
		return
	if from_email is None:
		from_email = 'reset@%s' % SITE_URL
	token = reset_token(user)
	subject = 'password reset for %s' % domain
	body = render_to_string('reset_email.html', {
		'domain': domain,
		'user': user,
		'token': token,
	}, RequestContext(request))
	send_mail(subject, body, from_email, [user.email])


