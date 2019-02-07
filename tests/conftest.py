import django
from django.conf import settings
from django.core import management
from django.test import Client
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
        ROOT_URLCONF='',
        ALLOWED_HOSTS=["*"],
    )
    django.setup()
    management.call_command("migrate")


@pytest.fixture
def client():
    yield Client()


@pytest.fixture(autouse=True)
def kerberos(monkeypatch):
    monkeypatch.setattr("kerberos.authGSSServerInit", lambda _: ("0", "ctx"))
    monkeypatch.setattr("kerberos.authGSSServerStep", lambda _, __: "0")
    monkeypatch.setattr("kerberos.authGSSServerUserName", lambda _: "admin")
    monkeypatch.setattr("kerberos.authGSSServerResponse", lambda _: "challenge")
