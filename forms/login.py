
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core import validators


User = get_user_model()
username_field = User.USERNAME_FIELD


class BaseLoginForm(forms.Form):

	#password = forms.CharField(widget = forms.PasswordInput)
	next = forms.CharField(max_length = 128, widget = forms.HiddenInput)

	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit', 'Login'))
		super(BaseLoginForm, self).__init__(*args, **kwargs)

	def clean(self):
		key = getattr(self, 'USERNAME_KEY', username_field)
		identifier = self.cleaned_data.get(key)
		password = self.cleaned_data.get('password')
		self.user = authenticate(username = identifier, password = password)
		if self.user is None:
			raise forms.ValidationError(
				message = 'there is no user with this %s and password combination' % key,
				code = 'invalid_login',
			)
		return self.cleaned_data


class EmailLoginForm(BaseLoginForm):

	email = forms.EmailField(max_length = 254)
	password = forms.CharField(widget = forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(EmailLoginForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs['placeholder'] = 'email@address.com'


class UsernameLoginForm(BaseLoginForm):

	username = forms.CharField(max_length = 30, validators = [validators.RegexValidator(
		r'^[\w.@+-]+$', 'Enter a valid username.', 'invalid')])
	password = forms.CharField(widget = forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(UsernameLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['placeholder'] = 'username'


class GenericLoginForm(BaseLoginForm):

	login = forms.CharField(max_length = 128)
	password = forms.CharField(widget = forms.PasswordInput)
	USERNAME_KEY = 'login'


if username_field == 'email':
	LoginForm = EmailLoginForm
elif username_field == 'username':
	LoginForm = UsernameLoginForm
else:
	LoginForm = GenericLoginForm


