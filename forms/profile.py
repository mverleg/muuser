
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django import forms
from django.core.urlresolvers import reverse


'''
	registration form, inspired by 
	http://stackoverflow.com/questions/16562529/django-1-5-usercreationform-custom-auth-model
'''
class ProfileForm(forms.ModelForm):
	
	class Meta:
		model = get_user_model()
		fields = get_user_model().PROFILE_FIELDS
	
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_action = 'profile_info'
		self.helper.add_input(Button(None, 'other settings', onclick = 'location.href=\'%s\'' % reverse('profile_actions'), tabindex = -1))
		self.helper.add_input(Submit('submit', 'change'))
		super(ProfileForm, self).__init__(*args, **kwargs)

class UserSettingsForm(ProfileForm):
	
	class Meta:
		model = get_user_model()
		fields = get_user_model().SETTINGS_FIELDS
	
	def __init__(self, *args, **kwargs):
		super(UserSettingsForm, self).__init__(*args, **kwargs)
		self.helper.form_action = 'profile_settings'


