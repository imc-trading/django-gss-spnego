import logging

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import View, RedirectView
from django.views.generic.base import ContextMixin, TemplateResponseMixin


logger = logging.getLogger(__name__)


class SpnegoHttpTemplate(TemplateResponse):
    def __init__(self, *args, **kwargs):
        super(SpnegoHttpTemplate, self).__init__(*args, **kwargs)
        self["WWW-Authenticate"] = "Negotiate"


class SpnegoView(View, ContextMixin, TemplateResponseMixin):
    http_method_names = ["get", "post", "put", "head", "options"]
    template_name = 'spnego.html'
    response_class = SpnegoHttpTemplate

    def get(self, request, *args, **kwargs):
        self._spnego_success = False
        request.gssresponse = None
        if "Negotiate" in request.META.get('HTTP_AUTHORIZATION', ""):
            user = authenticate(request, spnego=request.META["HTTP_AUTHORIZATION"].split()[1])
            if user:
                self._spnego_success = True
                login(request, user)
        return self.render_to_response(self.get_context_data(**kwargs), gssresponse=request.gssresponse)

    def get_context_data(self, **kwargs):
        ctx = super(SpnegoView, self).get_context_data(**kwargs)
        ctx.update({"spnego_succes": self._spnego_success})

    def render_to_response(self, context, **response_kwargs):
        gssstring = response_kwargs.pop("gssresponse", None)
        resp = super(SpnegoView, self).render_to_response(context, **response_kwargs)
        if self._spnego_success:
            resp["WWW-Authenticate"] = "Negotiate {}".format(gssstring)
            resp.status_code = 200
        else:
            resp.status_code = 401
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
