from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class UUIDPKMixin:
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
