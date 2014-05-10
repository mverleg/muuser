
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


'''
	registration form, inspired by http://stackoverflow.com/questions/16562529/django-1-5-usercreationform-custom-auth-model
'''
class PasswordForm(PasswordChangeForm):
	
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_action = 'profile_password'
		self.helper.add_input(Submit('submit', 'Change'))
		super(PasswordForm, self).__init__(*args, **kwargs)

'''
	see also the ResetPasswordForm in forms.reset
'''

