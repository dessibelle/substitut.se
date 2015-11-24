from __future__ import absolute_import
from .base import * # NOQA

TEST = True
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(SITE_ROOT, 'db.sqlite3')),
    }
}

INSTALLED_APPS = INSTALLED_APPS + (
    'django.contrib.staticfiles',
    'djangojs',
)

JASMINE_TEST_DIRECTORY = normpath(join(SITE_ROOT, 'jasmine'))

STATICFILES_DIRS += (
    ('js', normpath(join(SITE_ROOT, 'static', 'recipes', 'js'))),
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
