import os


TEST_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'price_monitor',
]

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(TEST_DIR, 'static')

SECRET_KEY = os.environ['SECRET_KEY']

ROOT_URLCONF = 'price_monitor.urls'

PRICE_MONITOR_AMAZON_PRODUCT_API_REGION = 'DE'
PRICE_MONITOR_AMAZON_PRODUCT_API_ASSOC_TAG = 'sample-assoc-tag'
