
from django.db.models.loading import get_model
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
import settings


'''
	if there are multiple user-derived models, you can set which
	is created by default durning registration with AUTH_USER_CREATE_MODEL
'''
def get_user_creation_model():
	if hasattr(settings, 'AUTH_USER_CREATE_MODEL'):
		app_label, model_name = getattr(settings, 'AUTH_USER_CREATE_MODEL').split('.')
		return get_model(app_label, model_name, seed_cache = False)
	return get_user_model()


'''
	registration form, inspired by http://stackoverflow.com/questions/16562529/django-1-5-usercreationform-custom-auth-model
'''
class RegistrationForm(forms.ModelForm):
	
	password = forms.CharField(label = 'Password', widget = forms.PasswordInput)
	password_confirm = forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput)
	next = forms.CharField(max_length = 128, widget = forms.HiddenInput)
	
	class Meta:
		model = get_user_creation_model()
		fields = ('email',)
	
	def clean_password_confirm(self):
		password = self.cleaned_data.get('password')
		password_confirm = self.cleaned_data.get('password_confirm')
		if not password == password_confirm:
			raise forms.ValidationError('The passwords are not the same!')
		return password
	
	def save(self, commit = True):
		user = super(RegistrationForm, self).save(commit = False)
		password = self.cleaned_data.get('password')
		user.set_password(password)
		if commit:
			user.save()
		return user
	
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_action = 'register'
		self.helper.add_input(Submit('submit', 'Register'))
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['email'].widget.attrs['placeholder'] = 'email@address.com'


