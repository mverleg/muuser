
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
	
	email = forms.EmailField(max_length = 254)
	password = forms.CharField(widget = forms.PasswordInput)
	next = forms.CharField(max_length = 128, widget = forms.HiddenInput)
	
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit', 'Login'))
		super(LoginForm, self).__init__(*args, **kwargs)
	
	def clean(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		self.user = authenticate(username = email, password = password)
		if self.user is None:
			raise forms.ValidationError(
				message = 'there is no user with this email and password combination',
				code = 'invalid_login',
			)
		return self.cleaned_data


