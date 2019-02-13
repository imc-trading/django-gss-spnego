import base64
import binascii
import gssapi
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
            token = base64.b64decode(spnego)
            credentials = gssapi.creds.Credentials(usage="accept")
            context = gssapi.SecurityContext(creds=credentials)
            response = context.step(token)
            if not context.complete:
                return None
            username = str(context.initiator_name)
            user = self.get_user_from_username(username)
            user.gssresponse = base64.b64encode(response).decode("utf-8")
            return user
        except gssapi.exceptions.GSSError as e:
            logger.warning("GSSAPI Error: %s", e, exc_info=settings.DEBUG)
            return None
        except (binascii.Error, TypeError):
            logger.warning("GSSAPI Error: Invalid base64 encoded token provided")
            return None


class SpnegoModelBackend(SpnegoBackendMixin, ModelBackend):
    @classmethod
    def get_user_from_username(cls, username):
        model = get_user_model()
        try:
            user, _ = model.objects.get_or_create(username=username.split("@")[0])
            return user
        except (model.DoesNotExist, model.MultipleObjectsReturned):
            return None
