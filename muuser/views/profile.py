
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login_required
from django.views.decorators.http import require_GET, require_POST
from mu3_user.forms.profile import ProfileForm
from mu3_user.forms.password import PasswordForm
from base.views.notification import notification


'''
	wrapper for django login view
'''
@require_GET
@login_required
def profile(request, *args, **kwargs):
	form_profile = ProfileForm(request.POST or None, instance = request.user)
	form_password = PasswordForm(request.user, request.POST or None)
	return render(request, 'profile.html', {
		'form_profile': form_profile,
		'form_password': form_password,
	})


@require_POST
@login_required
def profile_submit(request, *args, **kwargs):
	form_profile = ProfileForm(request.POST, instance = request.user)
	if form_profile.is_valid():
		form_profile.save()
		return redirect(to = reverse('profile'))
	return render(request, 'profile.html', {
		'form_profile': form_profile,
	})


@login_required
def profile_password(request, *args, **kwargs):
	if not request.method == 'POST':
		return redirect(to = reverse('profile'))
	form_password = PasswordForm(request.user, request.POST)
	if form_password.is_valid():
		form_password.save()
		return redirect(to = reverse('profile_password_done'))
	else:
		print 'invalid'
	return render(request, 'profile.html', {
		'form_password': form_password,
	})


@login_required
def profile_password_done(request, *args, **kwargs):
	return notification(request, message = 'Your password has been changed!', subject = 'Password changed', next = reverse('profile'))


