
from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm, ReadOnlyPasswordHashField
from django.forms.models import ModelForm
from django.forms.fields import EmailField, CharField
from django.forms.widgets import PasswordInput
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin
from muuser.models.user import MuUser


class MuUserChangeForm(ModelForm):
    
    email = EmailField(help_text = 'Required. Email address; also login name.')
    password = ReadOnlyPasswordHashField(help_text = 'Raw passwords are not stored, so there is no way to see this user\'s password, but you can change the password using <a href=\'password/\'>this form</a>.')
    
    class Meta:
        model = get_user_model()
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(MuUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
    
    def clean_password(self):
        ''' can't be changed directly '''
        print self.initial
        return self.initial['password']


class MuUserCreationForm(ModelForm):
    error_messages = {
        'duplicate_username': 'A user with that username already exists.',
        'password_mismatch': 'The two password fields didn\'t match.',
    }
    email = EmailField(help_text = 'Required. Email address; also login name.')
    password1 = CharField(label = 'Password', widget = PasswordInput)
    password2 = CharField(label = 'Password confirmation', widget = PasswordInput, help_text = 'Enter the same password as above, for verification.')
    
    class Meta:
        model = get_user_model()
        fields = ('email',)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'], code = 'password_mismatch')
        return password2
    
    def save(self, commit = True):
        user = super(MuUserCreationForm, self).save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class MuUserAdmin(UserAdmin):
    
    fieldsets = [
        ['Login', {'fields': ['email', 'password']}],
        ['Personal info', {'fields': ['first_name', 'last_name']}],
        ['Permissions', {'fields': ['is_staff', 'is_superuser', 'groups', 'user_permissions']}],
        #('Important dates', {'fields': ('last_login', 'date_joined')}),
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    list_display = ('get_full_name', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    
    form = MuUserChangeForm
    add_form = MuUserCreationForm
    change_password_form = AdminPasswordChangeForm
    
    class Meta:
		model = MuUser


#admin.site.register(MuUser, MuUserAdmin)


