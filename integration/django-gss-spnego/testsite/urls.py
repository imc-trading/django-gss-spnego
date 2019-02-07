from django.conf.urls import url
from django.contrib import admin

from django_gss_spnego.views import SpnegoLoginView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/spnego$', SpnegoLoginView.as_view(), name="spnego")
]
