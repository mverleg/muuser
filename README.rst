
Django Mu3 User
-----------

Django custom user that uses email as login name. Not directly usable, because it relies on mu3 and admin_settings, but available for adaptation or inspiration.

Future development
-----------

- Connect an OAuth account
- Email verification during registration
- Admin approval during registration

Installation & Configuration:
-----------

With an empty database (otherwise you will have to do some migration):

- Install using ``pip install git+https://mverleg@bitbucket.org/mverleg/django_mu3_user.git`` (or download and copy the app into your project)
- Include ``mu3_user`` in ``INSTALLED_APPS``
- Set ``CUSTOM_USER_MODEL`` to ``Mu3User`` or your derivative of ``Mu3UserAbstract``.
- Run ``manage.py syncdb``
- In ``urls.py`` add ``url(r'^account/', include(mu3_user.urls)),``

License
-----------

django_admin is available under the revised BSD license, see LICENSE.txt. You can do anything as long as you include the license, don't use my name for promotion and are aware that there is no warranty.


