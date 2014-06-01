
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login_required
from misc.views.notification import notification
from muuser.forms.password import PasswordForm
from django.views.decorators.http import require_GET


@login_required
def password(request):
	form = PasswordForm(request.user, request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect(to = reverse('profile_password_done'))
	return render(request, 'profile.html', {
		'header': 'Password',
		'form': form,
	})


@login_required
@require_GET
def password_done(request):
	return notification(request, message = 'Your password has been changed!', subject = 'Password changed', next = reverse('profile_actions'))


