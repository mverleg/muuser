# -*- coding: utf-8 -*-

'''
    for installing with pip
'''

from distutils.core import setup
from setuptools import find_packages

setup(
    name='muuser',
    version='1.0.0',
    author=u'Mark V',
    author_email='noreply.mail.nl',
    packages=find_packages(),
    include_package_data=True,
    url='git+https://bitbucket.org/mverleg/django_muuser',
    license='free to use without permission, but only at your own risc',
    description='Django Admin Settings lets you put site-wide settings for Django in the database and makes them editable easily through the admin interface. Staff members can be given fairly specific permissions to change settings.',
    zip_safe=True,
    install_requires = [],
)
