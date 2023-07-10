"""
Django settings for umibukela project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'true') == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = '-r&cjf5&l80y&(q_fiidd$-u7&o$=gv)s84=2^a2$o^&9aco0o'
else:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

GOOGLE_TAG_MANAGER = os.environ.get('GOOGLE_TAG_MANAGER')

HEALTHE_KOBO_USERNAME = os.environ.get('HEALTHE_KOBO_USERNAME')
HEALTHE_KOBO_PASSWORD = os.environ.get('HEALTHE_KOBO_PASSWORD')

BLACKSASH_KOBO_USERNAME = os.environ.get('BLACKSASH_KOBO_USERNAME')
BLACKSASH_KOBO_PASSWORD = os.environ.get('BLACKSASH_KOBO_PASSWORD')

KOBO_CLIENT_ID = os.environ.get('KOBO_CLIENT_ID')
KOBO_CLIENT_SECRET = os.environ.get('KOBO_CLIENT_SECRET')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'background_task',
    'pipeline',
    'django_extensions',
    'jsonfield',
    'django_markup',

    'umibukela',
)

MIDDLEWARE_CLASSES = (
    'umibukela.middleware.RedirectsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'umibukela.urls'

WSGI_APPLICATION = 'umibukela.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
LOGIN_REDIRECT_URL = '/'

CORS_ORIGIN_ALLOW_ALL = True
# NB This is necessary for people who've gotten a cookie from this domain
# and now want to view stockouts on an embedding site. It also means credentials
# may be sent to the URLs where we accept cross-origin requests, so we need
# to consider this when adding access-controlled resources to the the
# cross-origin-enabled URLs.
CORS_ALLOW_CREDENTIALS = True
CORS_URLS_REGEX = r'^/stockouts/.*$'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import dj_database_url
db_config = dj_database_url.config(default='postgres://umibukela:umibukela@localhost:5432/umibukela')
db_config['ATOMIC_REQUESTS'] = True
DATABASES = {
    'default': db_config,
}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# Caches
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/umibukela_cache',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Templates
TEMPLATE_DEBUG = DEBUG
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "umibukela.context_processors.general",
)

# file uploads
if DEBUG:
    DEFAULT_FILE_STORAGE = 'umibukela.dev_storage.DevFileSystemStorage'
    FAKE_MISSING_FILE_SIZE = True
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    DEFAULT_FILE_STORAGE = 'umibukela.botopatch.S3Storage'
    AWS_S3_FILE_OVERWRITE = False
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = "umibukela-media"
    AWS_S3_HOST = "s3-eu-west-1.amazonaws.com"
    AWS_HEADERS = {
        'Cache-Control': 'max-age=86400',
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

ASSETS_DEBUG = DEBUG
ASSETS_URL_EXPIRE = False

# assets must be placed in the 'static' dir of your Django app

# where the compiled assets go
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# the URL for assets
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
)

PYSCSS_LOAD_PATHS = [
    os.path.join(BASE_DIR, 'umibukela', 'static'),
    os.path.join(BASE_DIR, 'umibukela', 'static', 'bower_components'),
    os.path.join(BASE_DIR, 'umibukela', 'static', 'bower_components', 'bootstrap-sass', 'assets', 'stylesheets'),
    os.path.join(BASE_DIR, 'umibukela', 'static', 'bower_components', 'fontawesome', 'scss'),
]

PIPELINE_CSS = {
    'css': {
        'source_filenames': (
            'stylesheets/app.scss',
            'bower_components/fontawesome/css/font-awesome.css',
            'bower_components/leaflet/dist/leaflet.css',
        ),
        'output_filename': 'app.css',
    },
    'print-materials': {
        'source_filenames': (
            'stylesheets/print-materials.scss',
            'bower_components/fontawesome/css/font-awesome.css',
        ),
        'output_filename': 'print-materials.css',
    },
}
PIPELINE_JS = {
    'js': {
        'source_filenames': (
            'bower_components/jquery/dist/jquery.min.js',
            'bower_components/bootstrap-sass/assets/javascripts/bootstrap.min.js',
            'bower_components/jquery-stupid-table/stupidtable.min.js',
            'javascript/app.js',
        ),
        'output_filename': 'app.js',
    },
    'print-materials': {
        'source_filenames': (
            'bower_components/jquery/dist/jquery.min.js',
            'javascript/d3.min.js',
            'bower_components/underscore/underscore-min.js',
            'javascript/charts.js',
        ),
        'output_filename': 'print-materials.js',
    },
    'site': {
        'source_filenames': (
            'bower_components/leaflet/dist/leaflet.js',
            'bower_components/underscore/underscore-min.js',
            'javascript/highcharts.js',
            'javascript/site.js',
        ),
        'output_filename': 'site.js',
    },
    'survey-form': {
        'source_filenames': (
            'javascript/survey-form.js',
        ),
        'output_filename': 'survey-form.js',
    }
}
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None
# don't wrap javascript
# see https://github.com/cyberdelia/django-pipeline/blob/ea74ea43ec6caeb4ec46cdeb7d7d70598e64ad1d/pipeline/compressors/__init__.py#L62
PIPELINE_DISABLE_WRAPPER = True

PIPELINE_COMPILERS = (
    'umibukela.pipeline.PyScssCompiler',
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'umibukela.pipeline.GzipManifestPipelineStorage'


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR'
    },
    'loggers': {
        # put any custom loggers here
        'umibukela': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'django': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'requests': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    }
}
