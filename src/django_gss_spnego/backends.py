import kerberos
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

logger = logging.getLogger(__name__)


class SpnegoBackendMixin(object):
    def authenticate(self, request, spnego=None, **kwargs):
        if spnego is None:
            return super(SpnegoBackendMixin, self).authenticate(request, **kwargs)
        try:
            _, context = kerberos.authGSSServerInit(getattr(settings, "KERBEROS_SPN", ""))
            result = kerberos.authGSSServerStep(context, spnego)
            if not result:
                return None
            username = kerberos.authGSSServerUserName(context)
            user = self.get_user_from_username(username)
            user.gssresponse = kerberos.authGSSServerResponse(context)
            return user
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
