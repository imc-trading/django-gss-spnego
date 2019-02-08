import os
import random

import django
from django.conf import settings
from django.core import management
from django.test import Client
import k5test
import pytest


def pytest_configure(config):
    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        SITE_ID=1,
        SECRET_KEY='testing',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL="/static",
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    "debug": True,  # We want template errors to raise
                }
            },
        ],
        MIDDLEWARE=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django_gss_spnego',
        ],
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        AUTHENTICATION_BACKENDS = ['django_gss_spnego.backends.SpnegoModelBackend'],
        ROOT_URLCONF='tests.test_views',
        ALLOWED_HOSTS=["*"],
    )
    django.setup()
    management.call_command("migrate")


@pytest.fixture
def client():
    yield Client()


@pytest.fixture(scope="session", autouse=True)
def k5realm():
    k5realm = k5test.K5Realm(
        krb5_conf={'libdefaults': {'rdns': 'false'}},
        portbase=random.randint(1000, 6000) * 10,  # For tox parallel
    )
    os.environ.update(k5realm.env)
    yield k5realm
    for k in k5realm.env.keys():
        del os.environ[k]
    k5realm.stop()
    del k5realm
