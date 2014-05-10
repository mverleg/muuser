
from django.db import models
from django.core.validators import RegexValidator


class Address(models.Model):
	
	street_name = models.CharField(max_length = 64)
	street_nr = models.IntegerField()
	city = models.CharField(max_length = 32)
	postal_code = models.CharField(max_length = 32, blank = True, null = True, validators = [RegexValidator(regex = r'^[1-9][0-9]{3} ?[a-zA-Z]{2}$', message = 'enter a postal code like 1234 AB')])
	country = models.CharField(max_length = 32, default = 'Netherlands')
	
	longitude = models.FloatField(blank = True, null = True)
	latitude = models.FloatField(blank = True, null = True)
	
	def __unicode__(self):
		return '%s %s, %s, %s' % (self.street_name, self.street_nr, self.city, self.country)
	
	def google_name(self):
		if self.postal_code:
			return '%s %s, %s, %s, %s' % (self.street_name, self.street_nr, self.postal_code, self.city, self.country)
		else:
			return '%s %s, %s, %s' % (self.street_name, self.street_nr, self.city, self.country)
	
	def save(self, *args, **kwargs):
		if self.postal_code:
			if len(self.postal_code) == 6:
				self.postal_code = '%s %s' % (self.postal_code[:4], self.postal_code[-2:])
			self.postal_code = self.postal_code.upper()
		return super(Address, self).save(*args, **kwargs)
	
	class Meta:
		app_label = 'account'


