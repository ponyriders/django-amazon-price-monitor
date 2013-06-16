from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy


class EmailNotification(models.Model):
    """
    An email notification.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Owner'))
    email = models.EmailField(verbose_name=_('Email address'))

    def __unicode__(self):
        """
        Returns the unicode representation of the EmailNotification.
        :return: the unicode representation
        :rtype: unicode
        """
        return u'EmailNotification of %(user)s to %(email)s' % {
            'email': self.email,
            'user': self.owner.username,
        }

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Email Notification')
        verbose_name_plural = ugettext_lazy('Email Notifications')
