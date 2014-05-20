
from django.db import models
from django.core.validators import RegexValidator


#todo: there should be a better way to do this; model fields are redefined just to change blank=null=True

class BaseAddress(models.Model):
	
	postal_code = models.CharField(max_length = 32, blank = True, null = True, validators = [RegexValidator(regex = r'^[1-9][0-9]{3} ?[a-zA-Z]{2}$', message = 'enter a postal code like 1234 AB')])
	country = models.CharField(max_length = 32, default = 'Netherlands')
	
	longitude = models.FloatField(blank = True, null = True)
	latitude = models.FloatField(blank = True, null = True)
	
	def __unicode__(self):
		return '%s %s, %s, %s' % (self.street_name, self.street_nr, self.city, self.country)
	
	def google_address_search_name(self):
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


'''
	project needs to create an instance of this that is not abstract, 
	as it should not be added to the database unless used
'''
class MuAddress(BaseAddress):
	
	street_name = models.CharField(max_length = 64, null = True, blank = False)
	street_nr = models.IntegerField(null = True, blank = False)
	city = models.CharField(max_length = 32, null = True, blank = False)
	
	def google_name(self):
		return self.google_address_search_name()
				
	class Meta:
		app_label = 'account'
		abstract = True


'''
	this mixin simply adds the address fields to the user or other object itself
'''
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
