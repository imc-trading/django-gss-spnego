from django.conf.urls import url
from django.contrib import admin
from django_gss_spnego.views import SpnegoView
import base64
import gssapi

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^spnego$', SpnegoView.as_view(), name="spnego")
]

def test_initial_get(client):
    resp = client.get('/spnego')
    assert resp.status_code == 401

def test_failed_authentication(client):
    negotiate = "Negotiate BADSTRING"
    resp = client.get('/spnego', HTTP_AUTHORIZATION=negotiate)
    assert resp.status_code == 401

def test_authentication(client, k5realm):
    spn = gssapi.Name('host/{}'.format(k5realm.hostname), gssapi.raw.NameType.kerberos_principal)
    context = gssapi.SecurityContext(name=spn, usage='initiate')
    token = context.step()
    negotiate = "Negotiate {}".format(base64.b64encode(token).decode('utf-8'))
    resp = client.get('/spnego', HTTP_AUTHORIZATION=negotiate)
    context.step(base64.b64decode(resp['WWW-Authenticate'].split()[1]))
    assert context.complete
    assert resp.status_code == 200
    # Test a second authentication to make sure we bypass SPNEGO in an authenticated session
    resp = client.get('/spnego', HTTP_AUTHORIZATION=negotiate)
    assert resp.status_code == 200
