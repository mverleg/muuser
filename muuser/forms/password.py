
from django.contrib.auth.forms import PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from muuser.forms.reset import ResetPasswordForm


'''
	change password form
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
SetPasswordForm = ResetPasswordForm


