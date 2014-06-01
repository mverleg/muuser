
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from muuser.forms.login import LoginForm
from muuser.functions.next_get import next_GET
from django.contrib.auth import login as auth_login


@next_GET
def login(request, next):
	if request.user.is_authenticated():
		return redirect(to = reverse('logout'))
	form = LoginForm(data = request.POST or None, initial = {'next': next})
	if request.method == 'POST':
		if form.is_valid():
			auth_login(request, form.user)
			return redirect(to = form.cleaned_data['next'])
	return render(request, 'login.html', {
		'form': form,
		'next': next,
	})


