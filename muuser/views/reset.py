
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from mu3_user.functions.next_get import next_GET, next_GET_or
from mu3_user.forms.reset import RequestResetForm, ResetPasswordForm
from mu3_user.functions.reset import send_reset_link, reset_token
from django.contrib.auth import get_user_model
from base.views.notification import notification


'''
	request a password reset email
'''
@next_GET
def reset_request(request, *args, **kwargs):
	if request.user.is_authenticated():
		return render(request, 'reset_logged_in.html', {})
	form = RequestResetForm(request.POST or None)#, initial = {'next': next})
	if request.method == 'POST':
		if form.is_valid():
			''' send an email if the address exists; otherwise still pretend to '''
			users = get_user_model().objects.filter(email = form.cleaned_data['email'])
			if users:
				send_reset_link(request, users[0], request.get_host())
			return redirect(to = reverse('password_reset_sent'))
	return render(request, 'reset_request.html', {
		'form': form,
	})

'''
	password reset email has been sent
'''
@next_GET_or('login')
def reset_sent(request, *args, **kwargs):
	if request.user.is_authenticated():
		return render(request, 'reset_logged_in.html', {})
	return notification(request, message = '''<p>We've emailed you instructions for setting your password. You should be receiving them shortly.</p>
		<p>If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder.</p>
		''', subject = 'Check your mail', next = next)

'''
	the view that the emailed reset link directs to, that actually resets the password
'''
def reset_new(request, uid, token):
	if request.user.is_authenticated():
		return render(request, 'reset_logged_in.html', {})
	try:
		user = get_user_model().objects.get(pk = int(uid))
	except get_user_model().DoesNotExist:
		return notification(request, message = 'This password reset link is invalid because a user with id %d does not exist.' % int(uid), subject = 'User not found')
	if not token == reset_token(user):
		return notification(request, message = 'This is not a valid reset token for this user. This could happen if it has already been used.', subject = 'Invalid token', next = reverse('password_reset'))
	form = ResetPasswordForm(user = user, data = request.POST or None)
	if form.is_valid():
		form.save()
		return redirect(to = reverse('password_reset_complete'))
	return render(request, 'reset_new_password.html', {
		'form': form,
	})

'''
	password has been updated
'''
def reset_complete(request):
	if request.user.is_authenticated():
		return render(request, 'reset_logged_in.html', {})
	return notification(request, message = '''Your password has been set. You may go ahead and log in now.''', subject = 'New password set', next = reverse('login'))


