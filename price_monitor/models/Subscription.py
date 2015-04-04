from .mixins.PublicIDMixin import PublicIDMixin

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


class Subscription(PublicIDMixin, models.Model):
    """
    Model for a user being able to subscribe to a product and be notified if the price_limit is reached.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Owner'))
    product = models.ForeignKey('Product', verbose_name=_('Product'))
    price_limit = models.FloatField(verbose_name=_('Price limit'))
    date_last_notification = models.DateTimeField(null=True, blank=True, verbose_name=_('Date of last sent notification'))
    email_notification = models.ForeignKey('EmailNotification', verbose_name=_('Email Notification'))

    def get_email_address(self):
        """
        Returns the email address of the notification.
        :return: string
        """
        return self.email_notification.email
    get_email_address.short_description = ugettext_lazy('Notification email')

    def __str__(self):
        """
        Returns the string representation of the Subscription.
        :return: the unicode representation
        :rtype: unicode
        """
        return 'Subscription of "%(product)s" for %(user)s' % {
            'product': self.product.title,
            'user': self.owner.username,
        }

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Subscription')
        verbose_name_plural = ugettext_lazy('Subscriptions')
        ordering = ('product__title', 'price_limit', 'email_notification__email', )
