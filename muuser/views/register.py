
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from mu3_user.forms.register import RegistrationForm
from mu3_user.functions.next_get import next_GET_or
from base.views.notification import notification


'''
	wrapper for django login view
'''
@next_GET_or('profile')
def register(request, next, *args, **kwargs):
	if request.user.is_authenticated():
		return redirect(to = reverse('logout'))
	form = RegistrationForm(request.POST or None, initial = {'next': next})
	if request.method == 'POST':
		if form.is_valid():
			user = form.save()
			user = authenticate(username = user.email, password = form.cleaned_data['password'])
			login(request, user)
			return notification(request, message = 'Your account %s has been created! Welcome to the site!' % user.email, subject = 'Welcome, %s' % user, next = form.cleaned_data['next'])
	return render(request, 'register.html', {
		'form': form,
	})


