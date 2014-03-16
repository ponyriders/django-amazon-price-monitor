import os


TEST_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'price_monitor',
]

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(TEST_DIR, 'static')

SECRET_KEY = 'F(fxm_9aKa9F_7e$!U1can%;%qc9A[.Jcx2lVCwWo3}*DL,y?H'
