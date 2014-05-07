
'''
    create initial data for this model, on syncdb
    make sure to check if it doesn't yet exist
'''

from mu3_user.models.user import Mu3User
from admin_settings import Setting
from django.contrib.auth import get_user_model


INITIAL_USER = 'mark.verleg@gmail.com'

def initial_data(*args, **kwargs):
    '''
        create an admin user
    '''
    if not get_user_model().objects.filter(email = INITIAL_USER):
        get_user_model().objects.create_superuser(email = INITIAL_USER, password = 'admin').save()
        print 'created initual user \'%s\'; please change password a.s.a.p.' % INITIAL_USER
    
    '''
        initialize user setting(s)
    '''
    #if not Setting.objects.filter(name = 'DEFAULT_COUNTRY'):
    #    Setting(name = 'DEFAULT_COUNTRY', value = 'Netherlands', explanationn = 'the default').save()
    #    print 'created user settings'


