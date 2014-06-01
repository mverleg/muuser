
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from misc.views.notification import notification
from muuser.forms.register import RegistrationForm
from muuser.functions.next_get import next_GET_or


'''
	wrapper for django login view
'''
@next_GET_or('profile')
def register(request, next):
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


