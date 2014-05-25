
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from misc.views.notification import notification
from django.shortcuts import render


'''
	request a password reset email
'''
def email_unsubscribe(request, uid, token):
	
	try:
		user = get_user_model().objects.get(pk = int(uid))
	except get_user_model().DoesNotExist:
		return notification(request, message = 'This unsubscribe link is invalid because a user with id %d does not exist.' % int(uid), subject = 'User not found')
	
	if not token == user.email_unsubscribe_token():
		return notification(request, message = 'This is not a valid unsubscribe token for this user.', subject = 'Invalid token')
	
	if not user.receive_emails:
		return notification(request, message = 'You are already unsubscribed from these messages. If you still receive them, please contact the website owner. If you want to subscribe again, click next.', subject = 'Already unsubscribed', next = reverse('email_subscribe'))
	
	user.receive_emails = False
	user.save()
	
	return notification(request, message = 'You have been unsubscribed and will now only receive essential emails from this site. To subscribe again, click next.', subject = 'You have been unsubscribed', next = reverse('email_subscribe'))


@login_required
def email_subscribe(request):
	
	if request.user.receive_emails:
		return notification(request, message = 'You are already subscribed to these messages. If you do not want to receive them, you can unsubscribe by clicking next.', subject = 'Already subscribed', next = reverse('email_unsubscribe', kwargs = {'uid': request.user.pk, 'token': request.user.email_unsubscribe_token()}))
	
	if request.method == 'POST':
		request.user.receive_emails = True
		request.user.save()
		return notification(request, message = 'You have been subscribed to email messages from this site. Hopefully you will find them helpful, otherwise you can unsubscribe at any time.', subject = 'You have been subscribed', next = reverse('email_unsubscribe', kwargs = {'uid': request.user.pk, 'token': request.user.email_unsubscribe_token()}))
	
	return render(request, 'email_subscribe.html', {})


