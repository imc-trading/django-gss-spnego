from django.urls import re_path
from django.contrib import admin
from django_gss_spnego.views import SpnegoView, SpnegoRedirectView, SpnegoLoginView
import base64

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^spnego$", SpnegoView.as_view(), name="spnego"),
    re_path(r"^redirect$", SpnegoRedirectView.as_view(), name="redirect"),
    re_path(r"^login$", SpnegoLoginView.as_view(), name="login"),
]


def test_initial_get(client):
    resp = client.get("/spnego")
    assert resp.status_code == 401


def test_failed_authentication(client):
    negotiate = "Negotiate {}".format(base64.b64encode(b"BAD TOKEN").decode("utf-8"))
    resp = client.get("/spnego", HTTP_AUTHORIZATION=negotiate)
    assert resp.status_code == 401


def test_authentication(client, k5ctx):
    token = k5ctx.step()
    negotiate = "Negotiate {}".format(base64.b64encode(token).decode("utf-8"))
    resp = client.get("/spnego", HTTP_AUTHORIZATION=negotiate)
    if "WWW-Authenticate" in resp:
        k5ctx.step(base64.b64decode(resp["WWW-Authenticate"].split()[1]))
    assert k5ctx.complete
    assert resp.status_code == 200
    # Test a second authentication to make sure we bypass SPNEGO in an authenticated session
    resp = client.get("/spnego", HTTP_AUTHORIZATION=negotiate)
    assert resp.status_code == 200


def test_redirect(client, k5ctx):
    token = k5ctx.step()
    negotiate = "Negotiate {}".format(base64.b64encode(token).decode("utf-8"))
    resp = client.get("/redirect", HTTP_AUTHORIZATION=negotiate)
    if "WWW-Authenticate" in resp:
        k5ctx.step(base64.b64decode(resp["WWW-Authenticate"].split()[1]))
    assert k5ctx.complete
    assert resp.status_code == 302
    assert resp.url == "/admin/"


def test_failed_redirect(client):
    negotiate = "Negotiate BADSTRING"
    resp = client.get("/redirect", HTTP_AUTHORIZATION=negotiate)
    assert resp.status_code == 401


def test_login(client, k5ctx):
    token = k5ctx.step()
    negotiate = "Negotiate {}".format(base64.b64encode(token).decode("utf-8"))
    resp = client.get("/login", HTTP_AUTHORIZATION=negotiate)
    if "WWW-Authenticate" in resp:
        k5ctx.step(base64.b64decode(resp["WWW-Authenticate"].split()[1]))
    assert k5ctx.complete
    assert resp.status_code == 302
    assert resp.url == "/accounts/profile/"
