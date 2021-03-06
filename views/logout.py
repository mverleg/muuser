
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from muuser.forms.logout import LogoutForm
from django.contrib.auth import logout as auth_logout
from muuser.functions.next_get import next_GET
from misc.functions.secure import desecure_redirect
from . import settings


'''
	logs out user through a form (to prevent csrf)
'''
@next_GET
def logout(request, next):
	if not request.user.is_authenticated():
		return redirect(to = reverse('login'))
	form = LogoutForm(data = request.POST or None, initial = {'next': next})
	if request.method == 'POST':
		if form.is_valid():
			auth_logout(request)
			if getattr(settings, 'DESECURE_AFTER_LOGOUT', False):
				return desecure_redirect(request, form.cleaned_data['next'])
			else:
				return redirect(to = form.cleaned_data['next'])
	return render(request, 'logout.html', {
		'form': form,
	})


