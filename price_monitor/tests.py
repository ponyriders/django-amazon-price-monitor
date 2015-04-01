from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from price_monitor import utils
from price_monitor.models import (
    EmailNotification,
    Product,
    Subscription,
)

from testfixtures import log_capture


class ProductTest(TestCase):

    def test_set_failed_to_sync(self):
        asin = 'ASINASINASIN'
        p = Product.objects.create(asin=asin)
        self.assertIsNotNone(p)
        self.assertEqual(asin, p.asin)
        self.assertEqual(0, p.status)

        p.set_failed_to_sync()
        self.assertEqual(2, p.status)


class SubscriptionTest(TestCase):
    """
    Test class for the Subscription model.
    """
    urls = 'price_monitor.urls'

    def setUp(self):
        self.products = [
            Product.objects.create(asin='A1'),
            Product.objects.create(asin='A2'),
            Product.objects.create(asin='A3'),
        ]

    def tearDown(self):
        for p in self.products:
            p.delete()

    def test_delete_subscription(self):
        """
        Tests the deletion of an subscription via the delete_subscription_view.
        """
        # create a test user that is the subscription owner
        user_username = 'john'
        user_password = 'p4ssw0rd'
        owner = User.objects.create_user(user_username, 'john@example.com', user_password)

        # add his email notification
        email_notification = EmailNotification.objects.create(
            owner=owner,
            email='dummy@example.com',
        )

        # create a subscription for a product
        s = Subscription.objects.create(
            owner=owner,
            product=self.products[0],
            price_limit=10.0,
            email_notification=email_notification
        )

        # check that it's there
        self.assertTrue(s)
        self.assertTrue(len(s.public_id) == 36)

        # log the user in, requires django.contrib.sessions in INSTALLED_APPS
        self.assertTrue(
            self.client.login(username=user_username, password=user_password)
        )

        # get url for deletion and call it
        response = self.client.get(
            reverse('delete_subscription_view', kwargs={'public_id': s.public_id}),
            follow=True
        )

        # should be successful
        self.assertEqual(response.status_code, 200)

        # subscription shall be deleted now
        self.assertRaises(Subscription.DoesNotExist, lambda: Subscription.objects.get(public_id=s.public_id))


class UtilsTest(TestCase):
    """
    Tests for the utils module.
    """

    def test_get_offer_url(self):
        self.assertEqual('http://www.amazon.de/dp/X1234567890/?tag=sample-assoc-tag', utils.get_offer_url('X1234567890'))

    @log_capture()
    def test_parse_audience_rating(self, lc):
        """
        Tests the audience rating parse function.
        """
        self.assertEqual(0, utils.parse_audience_rating('Freigegeben ohne Altersbeschränkung'))
        lc.check()

        self.assertEqual(6, utils.parse_audience_rating('Freigegeben ab 6 Jahren'))
        lc.check()

        self.assertEqual(16, utils.parse_audience_rating('Freigegeben ab 16 Jahren'))
        lc.check()

        self.assertEqual(18, utils.parse_audience_rating('Freigegeben ab 18 Jahren'))
        lc.check()

        self.assertEqual('Unknown value', utils.parse_audience_rating('Unknown value'))
        lc.check(
            ('price_monitor.utils', 'ERROR', 'Unable to parse audience rating value "Unknown value"')
        )
