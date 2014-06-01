
from django.contrib.auth.forms import SetPasswordForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth import authenticate
from django import forms


'''
	request a reset email to be sent (doesn't check if the 
	address belongs to a user, because the user isn't allowed
	to know that unless it's his own)
'''
class RequestResetForm(forms.Form):
	
	email = forms.EmailField(max_length = 254)
	#next = forms.CharField(max_length = 128, widget = forms.HiddenInput)
	
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_action = 'password_reset'
		self.helper.add_input(Submit('submit', 'Request reset'))
		super(RequestResetForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs['placeholder'] = 'email@address.com'


'''
	enter a new password without entering the old one
'''
class ResetPasswordForm(SetPasswordForm):
	
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_action = ''
		self.helper.add_input(Submit('submit', 'Change'))
		super(ResetPasswordForm, self).__init__(*args, **kwargs)

