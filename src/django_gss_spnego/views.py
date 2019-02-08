import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import View, RedirectView
from django.views.generic.base import ContextMixin, TemplateResponseMixin


logger = logging.getLogger(__name__)


class SpnegoHttpTemplate(TemplateResponse):
    status_code = 401

    def __init__(self, *args, **kwargs):
        super(SpnegoHttpTemplate, self).__init__(*args, **kwargs)
        self["WWW-Authenticate"] = "Negotiate"


class SpnegoAuthMixin(object):
    def get(self, request, *args, **kwargs):
        self._spnego_success = False
        self._gssresponse = ""
        if not request.user.is_authenticated:
            if "Negotiate" in request.META.get("HTTP_AUTHORIZATION", ""):
                user = authenticate(
                    request, spnego=request.META["HTTP_AUTHORIZATION"].split()[1]
                )
                if user:
                    self._spnego_success = True
                    self._gssresponse = user.gssresponse
                    login(request, user)
        else:
            self._spnego_success = True
        return super(SpnegoAuthMixin, self).get(request, *args, **kwargs)


class SpnegoViewMixin(object):
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        ctx = super(SpnegoViewMixin, self).get_context_data(**kwargs)
        ctx.update({"spnego_success": self._spnego_success})


class SpnegoView(
    SpnegoAuthMixin, SpnegoViewMixin, ContextMixin, TemplateResponseMixin, View
):
    http_method_names = ["get", "post", "put", "head", "options"]
    response_class = SpnegoHttpTemplate
    template_name = "spnego.html"

    def render_to_response(self, context, **response_kwargs):
        resp = super(SpnegoView, self).render_to_response(context, **response_kwargs)
        if self._spnego_success:
            if self._gssresponse:
                resp["WWW-Authenticate"] = "Negotiate {}".format(self._gssresponse)
            resp.status_code = 200
        return resp


class SpnegoLoginView(SpnegoAuthMixin, SpnegoViewMixin, LoginView):
    http_method_names = ["get", "post", "put", "head", "options"]
    response_class = SpnegoHttpTemplate
    template_name = "spnego.html"

    def get(self, request, *args, **kwargs):
        resp = super(SpnegoLoginView, self).get(request, *args, **kwargs)
        if self._spnego_success:
            resp = HttpResponseRedirect(self.get_success_url())
            if self._gssresponse:
                resp["WWW-Authenticate"] = "Negotiate {}".format(self._gssresponse)
        return resp


class SpnegoRedirectView(SpnegoView, RedirectView):
    pattern_name = "admin:index"

    def get(self, request, *args, **kwargs):
        orig_resp = super(SpnegoRedirectView, self).get(request, *args, **kwargs)
        if orig_resp.status_code == 401:
            return orig_resp
        else:
            new_resp = HttpResponseRedirect(self.get_redirect_url(*args, **kwargs))
            new_resp["WWW-Authenticate"] = orig_resp["WWW-Authenticate"]
            return new_resp
