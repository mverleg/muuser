
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.views import login_required
from muuser.forms.password import PasswordForm
from muuser.forms.profile import ProfileForm, UserSettingsForm
from muuser.forms.logout import LogoutForm


@login_required
def actions(request):
	logout_form = LogoutForm(data = request.POST or None, initial = {'next': reverse('login')})
	return render(request, 'profile_actions.html', {
		'logout_form': logout_form,
	})
	#profile_form = ProfileForm(request.POST or None, instance = request.user)
	#settings_form = UserSettingsForm(request.POST or None, instance = request.user)
	#password_form = PasswordForm(request.user, request.POST or None)
	#return render(request, 'profile_actions.html', {
	#	'profile_form': profile_form,
	#	'settings_form': settings_form,
	#	'password_form': password_form,
	#})


