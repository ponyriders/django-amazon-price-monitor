import uuid

from django.db import models
from django.utils.translation import ugettext as _


class PublicIDMixin(models.Model):
    """
    Mixin for addind a public id to models to prevent revealing database ids via API
    """
    public_id = models.CharField(
        max_length=36,
        default=str(uuid.uuid4()),
        unique=True,
        editable=False,
        null=False,
        db_index=True,
        verbose_name=_('Public-ID')
    )

    class Meta:
        abstract = True
        app_label = 'price_monitor'
