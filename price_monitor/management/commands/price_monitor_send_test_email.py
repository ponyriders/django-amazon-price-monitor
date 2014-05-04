from ...utils import send_mail

from django.core.management.base import (
    BaseCommand,
    CommandError,
)


class Command(BaseCommand):
    """
    Command for sending a test mail as it is send through the system upon notification.
    """
    args = '<email>'
    help = 'Sends a test mail a test mail as it is send through the system upon notification.'

    def handle(self, *args, **options):
        """
        The magic happens here.
        """
        if len(args) != 1:
            raise CommandError('Please enter an email address to send the test email to!')

        send_mail(
            'A Sample Product Title',
            15.99,
            'EUR',
            11.49,
            'http://a.sample.offer.url/some/segment/',
            args[0]
        )
