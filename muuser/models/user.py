
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


'''
	a manager that doesn't use username when creating users
'''
class MuUserManager(UserManager):
	
	def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
		email = self.normalize_email(email)
		user = self.model(email = email, is_staff = is_staff, is_superuser = is_superuser, **extra_fields)
		user.set_password(password)
		user.save(using = self._db)
		return user
	
	def create_user(self, email, password = None, **extra_fields):
		return self._create_user(email = email, password = password, is_staff = False, is_superuser = False, **extra_fields)
	
	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email = email, password = password, is_staff = True, is_superuser = True, **extra_fields)


'''
	custom user model
'''
class MuUserAbstract(AbstractBaseUser, PermissionsMixin):
	
	''' personal fields (password is in base user) '''
	email = models.EmailField(blank = True, unique = True, help_text = 'Email address; also used as login name.')
	first_name = models.CharField(max_length = 30, blank = True)
	last_name = models.CharField(max_length = 30, blank = True)
	
	''' permissions and tracking '''
	is_staff = models.BooleanField(default = False, help_text = 'Designates whether the user can log into this admin site.')
	
	objects = MuUserManager()
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	
	class Meta:
		abstract = True
		app_label = 'muuser'
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


class MuUser(MuUserAbstract):
	pass


