
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login_required
from muuser.forms.profile import ProfileForm


@login_required
def profile(request):
	form = ProfileForm(request.POST or None, instance = request.user)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect(to = reverse('profile'))
	return render(request, 'profile.html', {
		'header': 'My info',
		'form': form,
	})


