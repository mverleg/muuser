
from django.contrib import admin
from muuser.models.address import MuAddress
from muuser.admin.user import MuUserAdmin
from django.contrib.admin.options import ModelAdmin


'''
	fields for the address admin (incl/especially mixin)
'''
ADDRESS_FIELDSET = ('street_name', 'street_nr', 'postal_code', 'city', 'country', 'longitude', 'latitude',)
ADDRESS_READONLY_FIELDS = ('longitude', 'latitude',)

'''
	admin for the separate address field
	registration in admin should happen in project.account, if applicable
'''
class AddressAdmin(ModelAdmin):
	
	model = MuAddress
	fields = ADDRESS_FIELDSET
	readonly_fields = ADDRESS_READONLY_FIELDS

'''
	mixin admin doesn't work well (how to extend fieldset/fields for generic subclass?)
'''


