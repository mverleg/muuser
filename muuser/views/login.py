
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from mu3_user.forms.login import LoginForm
from mu3_user.functions.next_get import next_GET
from django.contrib.auth import login as auth_login


'''
	wrapper for django login view
'''
@next_GET
def login(request, next, *args, **kwargs):
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


