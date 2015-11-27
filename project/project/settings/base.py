"""Common settings and globals."""

from os.path import abspath, basename, dirname, join, normpath
from sys import path

# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

TEST = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Dan Larsson', 'dan.larsson@substitut.se'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/Stockholm'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'sv-SE'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/assets/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    # static/lib -> assets/lib
    ('lib', normpath(join(SITE_ROOT, 'static', 'lib'))),
    # static/recipes/css -> assets/css
    ('css', normpath(join(SITE_ROOT, 'static', 'recipes', 'css'))),
    # sass -> assets/sass/recipes
    ('sass', normpath(join(SITE_ROOT, 'sass'))),
    # static/recipes/fonts/ -> assets/css
    ('css', normpath(join(SITE_ROOT, 'static', 'recipes', 'fonts'))),
    # static/recipes/js -> assets/js
    ('js', normpath(join(SITE_ROOT, 'static', 'recipes', 'js'))),
    # static/recipes/images/site -> assets/images/site
    (join('images', 'site'), normpath(join(SITE_ROOT, 'static', 'recipes', 'images', 'site'))),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r"luq=5fb^f_n)e838lq8b5(u*ps4y5t2eqjr3vstq%@s@k!g6a1"

# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'grappelli',
    'django.contrib.admin',
    'simplejson',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'sorl.thumbnail',
    'pipeline'
)
LOCAL_APPS = (
    'recipes',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

# django-pipeline settings

# see: http://django-pipeline.readthedocs.org/en/latest/configuration.html#pipeline-template-ext
PIPELINE_TEMPLATE_EXT = '.handlebars'

# see: http://django-pipeline.readthedocs.org/en/latest/configuration.html#pipeline-template-func
PIPELINE_TEMPLATE_FUNC = 'Handlebars.compile'

# see: http://django-pipeline.readthedocs.org/en/latest/configuration.html#pipeline-template-namespace
PIPELINE_TEMPLATE_NAMESPACE = 'Handlebars.templates'

# see: http://django-pipeline.readthedocs.org/en/latest/compressors.html
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'

# see: http://django-pipeline.readthedocs.org/en/latest/compilers.html
PIPELINE_COMPILERS = (
    'pipeline.compilers.sass.SASSCompiler',
)

# see: http://django-pipeline.readthedocs.org/en/latest/storages.html
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# see: http://django-pipeline.readthedocs.org/en/latest/configuration.html
PIPELINE_JS = {
    'app': {
        'source_filenames': (
            'js/init.js',
            'js/templates/*.handlebars',
            'js/exceptions.js',
            'js/handlebars_helpers.js',
            'js/recipe.js',
            'js/responsive.js',
            'js/storage.js',
            'js/vote.js',
            'js/security.js',
            'js/substitut.js',
            'js/main.js',
        ),
        'output_filename': 'js/app.js',
    },
    'vendor': {
        'source_filenames': (
            'lib/jquery/dist/jquery.min.js',
            'lib/jquery-ui/jquery-ui.min.js',
            'lib/hisrc/hisrc.js',
            'lib/handlebars/handlebars.js',
            'lib/parallax/parallax.min.js',
            'lib/bootstrap-sass/assets/javascripts/bootstrap.min.js',
            'lib/Flowtype.js/flowtype.js',
        ),
        'output_filename': 'js/vendor.js',
    }

}
PIPELINE_CSS = {
    'app': {
        'source_filenames': (
            'sass/app.scss',
        ),
        'output_filename': 'css/app.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}

# sorl-thumbnail settings

# see: https://sorl-thumbnail.readthedocs.org/en/latest/reference/settings.html#thumbnail-format
THUMBNAIL_FORMAT = 'PNG'

# see: https://sorl-thumbnail.readthedocs.org/en/latest/reference/settings.html#thumbnail-kvstore
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'

# see: https://sorl-thumbnail.readthedocs.org/en/latest/reference/settings.html#thumbnail-redis-host
THUMBNAIL_REDIS_HOST = 'localhost'

# see: https://sorl-thumbnail.readthedocs.org/en/latest/reference/settings.html#thumbnail-redis-port
THUMBNAIL_REDIS_PORT = 6379

SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

# number of recipes per page
PAGE_LIMIT = 5

# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(SITE_ROOT, 'db.sqlite3'),
    }
}
