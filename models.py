
from django.contrib.auth.hashers import get_hasher
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from re import sub
from django.db import models
from django.core.validators import RegexValidator


"""
	Custom user model.
"""
class svUser(AbstractBaseUser, PermissionsMixin):

	email = models.EmailField(blank = True, unique = True, max_length = 254, help_text = 'Email address; also used as login name.')
	first_name = models.CharField(max_length = 30, blank = True)
	last_name = models.CharField(max_length = 30, blank = True)

	receive_emails = models.BooleanField(default = True, help_text = 'Turn off to receive only essential emails')
	is_staff = models.BooleanField(default = False, help_text = 'Designates whether the user can log into this admin site.')

	objects = svUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	PROFILE_FIELDS = ('first_name', 'last_name',)
	SETTINGS_FIELDS = ('receive_emails',)

	class Meta:
		app_label = 'account'
		verbose_name = 'user'
		verbose_name_plural = 'users'

	def __unicode__(self):
		return self.get_full_name()

	def email_name(self):
		return self.email.split('@')[0].replace('_', ' ').replace('-', ' ').replace('.', ' ').replace('  ', ' ').title()

	def get_short_name(self):
		name = self.first_name.strip()
		if not name:
			return self.email_name()
		return name

	def get_full_name(self):
		name = ('%s %s' % (self.first_name, self.last_name)).strip()
		if not name:
			return self.email_name()
		return name

	def email_unsubscribe_token(self):
		token = get_hasher().encode(self.email, 'unsubscribe')
		token = sub(r'[^a-zA-Z0-9]+', '', token.split('$')[-1])
		return token[-12:]


"""
	A manager that doesn't use username when creating users.
"""
class svUserManager(UserManager):

	def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
		email = self.normalize_email(email)
		user = self.model(email = email, is_staff = is_staff, is_superuser = is_superuser, **extra_fields)
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_user(self, email, password = None, **extra_fields):
		return self._create_user(email = email, password = password, is_staff = False, is_superuser = False, **extra_fields)

	def create_nologin_user(self, email, **extra_fields):
		user = self._create_user(email = email, is_staff = False, is_superuser = False, **extra_fields)
		user.set_unusable_password()
		return user

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email = email, password = password, is_staff = True, is_superuser = True, **extra_fields)


#todo: there should be a better way to do this; model fields are redefined just to change blank=null=True

class BaseAddress(models.Model):

	postal_code = models.CharField(max_length = 32, blank = True, null = True, validators = [RegexValidator(regex = r'^[1-9][0-9]{3} ?[a-zA-Z]{2}$', message = 'enter a postal code like 1234 AB')])
	country = models.CharField(max_length = 32, default = 'Netherlands')

	longitude = models.FloatField(blank = True, null = True)
	latitude = models.FloatField(blank = True, null = True)

	def __unicode__(self):
		return '%s %s, %s, %s' % (self.street_name, self.street_nr, self.city, self.country)

	def full_address(self):
		if self.postal_code:
			return '%s %s, %s, %s, %s' % (self.street_name, self.street_nr, self.postal_code, self.city, self.country)
		else:
			return '%s %s, %s, %s' % (self.street_name, self.street_nr, self.city, self.country)

	def save(self, *args, **kwargs):
		if self.postal_code:
			if len(self.postal_code) == 6:
				self.postal_code = '%s %s' % (self.postal_code[:4], self.postal_code[-2:])
			self.postal_code = self.postal_code.upper()
		return super(BaseAddress, self).save(*args, **kwargs)

	class Meta:
		app_label = 'account'
		abstract = True


"""
	Project needs to create an instance of this that is not abstract,
	as it should not be added to the database unless used.
"""
class MuAddress(BaseAddress):

	street_name = models.CharField(max_length = 64, null = True, blank = False)
	street_nr = models.IntegerField(null = True, blank = False)
	city = models.CharField(max_length = 32, null = True, blank = False)

	class Meta:
		app_label = 'account'
		abstract = True


"""
	This mixin simply adds the address fields to the user or other object itself.
"""
class AddressMixin(BaseAddress):

	street_name = models.CharField(max_length = 64, null = True, blank = False)
	street_nr = models.IntegerField(null = True, blank = False)
	city = models.CharField(max_length = 32, null = True, blank = False)

	class Meta:
		app_label = 'account'
		abstract = True


class AddressOptionalMixin(BaseAddress):

	street_name = models.CharField(max_length = 64, null = True, blank = True)
	street_nr = models.IntegerField(null = True, blank = True)
	city = models.CharField(max_length = 32, null = True, blank = True)

	class Meta:
		app_label = 'account'
		abstract = True


