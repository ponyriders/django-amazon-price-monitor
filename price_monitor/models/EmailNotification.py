from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


class EmailNotification(models.Model):
    """
    An email notification.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Owner'))
    email = models.EmailField(verbose_name=_('Email address'))

    def notify(self, subscription):
        """
        Sends an email notification to the subscriber.
        :param subscription: the subscription matching the subscriber and the product.
        """
        # TODO remove and continue
        return

        send_mail(
            _('Price limit for %(product)s reached' % {'product': subscription.product.title}),
            _(
                'The price limit of %(price_limit)s %(currency)s has been reached for the article %(product_title)s.\nYou can support our platform by using '
                'this link for buying: %(link)s\n\n\nRegards,\nThe Team' % {
                    'price_limit': None,
                    'currency': None,
                    'product_title': None,
                    'link': None,
                }
            ),
            'sender',
            'recv',
            fail_silently=False,
        )

    def __unicode__(self):
        """
        Returns the unicode representation of the EmailNotification.
        :return: the unicode representation
        :rtype: unicode
        """
        return u' %(email)s' % {
            'email': self.email,
        }

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Email Notification')
        verbose_name_plural = ugettext_lazy('Email Notifications')
