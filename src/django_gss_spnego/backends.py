import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

try:
    import kerberos
except ImportError:
    import winkerberos as kerberos

logger = logging.getLogger(__name__)


class SpnegoBackendMixin(object):
    def authenticate(self, request, spnego=None, **kwargs):
        if spnego is None:
            return super(SpnegoBackendMixin, self).authenticate(request, **kwargs)
        try:
            _, context = kerberos.authGSSServerInit(settings.KERBEROS_SPN or "")
            result = kerberos.authGSSServerStep(context, spnego)
            if not result:
                return None
            request.gssresponse = kerberos.authGSSServerResponse(context)
            username = kerberos.authGSSServerUserName(context)
            return self.get_user_from_username(username)
        except kerberos.GSSError:
            logger.exception("Kerberos error!")
            return None


class SpnegoModelBackend(SpnegoBackendMixin, ModelBackend):
    def get_user_from_username(self, username):
        model = get_user_model()
        try:
            user, _ = model.objects.get_or_create(username=username.split("@")[0])
            return user
        except (model.DoesNotExist, model.MultipleObjectsReturned):
            return None
