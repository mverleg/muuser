
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login_required
from muuser.forms.profile import UserSettingsForm


@login_required
def settings(request):
	form = UserSettingsForm(request.POST or None, instance = request.user)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect(to = reverse('profile_settings'))
	return render(request, 'profile.html', {
		'header': 'Preferences',
		'form': form,
	})


