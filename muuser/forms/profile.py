
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


'''
	registration form, inspired by 
	http://stackoverflow.com/questions/16562529/django-1-5-usercreationform-custom-auth-model
'''
class ProfileForm(forms.ModelForm):
	
	class Meta:
		model = get_user_model()
		fields = ('first_name', 'last_name',)
	
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_action = 'profile_submit'
		self.helper.add_input(Submit('submit', 'Change'))
		super(ProfileForm, self).__init__(*args, **kwargs)
		#self.fields['email'].required = True


