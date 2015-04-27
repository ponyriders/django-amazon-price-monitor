from django.db import models
from django.utils.translation import ugettext as _

from uuid import uuid4


class PublicIDMixin(models.Model):
    """
    Mixin for addind a public id to models to prevent revealing database ids via API
    """
    public_id = models.CharField(
        max_length=36,
        unique=True,
        editable=False,
        null=False,
        db_index=True,
        verbose_name=_('Public-ID')
    )

    def save(self, *args, **kwargs):
        """
        Sets public id on new instances
        :param args: positional arguments
        :type args: list
        :param kwargs: keyword arguments
        :type kwargs: dict
        :returns: what parent returns
        :rtype: see parent
        """
        if self.pk is None:
            self.public_id = str(uuid4())
        return super(PublicIDMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'price_monitor'
