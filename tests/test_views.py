from django.conf.urls import url
from django.contrib import admin
from django.test import override_settings
from django_gss_spnego.views import SpnegoView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^spnego$', SpnegoView.as_view(), name="spnego")
]

@override_settings(ROOT_URLCONF='tests.test_views')
def test_initial_get(client):
    resp = client.get('/spnego')
    assert resp.status_code == 401

@override_settings(ROOT_URLCONF='tests.test_views')
def test_authentication(client):
    resp = client.get('/spnego', HTTP_AUTHORIZATION="Negotiate FakeString")
    assert resp.status_code == 200

@override_settings(ROOT_URLCONF='tests.test_views')
def test_repeated_authentication(client):
    client.get('/spnego', HTTP_AUTHORIZATION="Negotiate FakeString")
    resp = client.get('/spnego', HTTP_AUTHORIZATION="Negotiate FakeString")
    assert resp.status_code == 200
