"""Management command for sending a pricemonitor specific test email"""
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from price_monitor.models import (
    EmailNotification,
    Price,
    Product,
    Subscription,
)
from price_monitor.utils import send_mail


class Command(BaseCommand):

    """Command for sending a pricemonitor specific test email"""

    help = 'Sends a pricemonitor specific test email'

    def add_arguments(self, parser):
        """
        Adds the positional argument for the email address.

        :param parser: the argument parser
        """
        parser.add_argument('email', nargs='+', type=str)

    def handle(self, *args, **options):
        """Sends an email."""

        u = User()

        e = EmailNotification()
        e.owner = u
        e.email = options['email'][0]

        p = Product()
        p.asin = 'ASIN123'
        p.title = 'Dummy Product'
        p.offer_url = 'http://localhost/offer'

        s = Subscription()
        s.price_limit = 9.99
        s.email_notification = e

        r = Price()
        r.value = 8.00
        r.currency = 'EUR'
        r.date_seen = datetime.now()
        r.product = p

        send_mail(
            p,
            s,
            r,
            additional_text='This is a test email.'
        )
