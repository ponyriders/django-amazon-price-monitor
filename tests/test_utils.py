"""Tests for the utils module."""
from django.test import TestCase

from price_monitor import utils


class UtilsTest(TestCase):

    """Tests for the utils module."""

    def test_get_offer_url(self):
        """Test the offer url function"""
        self.assertEqual('http://www.amazon.de/dp/X1234567890/?tag=sample-assoc-tag', utils.get_offer_url('X1234567890'))

    def test_chunk_list(self):
        """Tests the chunk_list function"""
        self.assertEqual(
            [[10, 11, 12, 13], [14, 15, 16, 17], [18, 19]],
            list(utils.chunk_list(list(range(10, 20)), 4))
        )
        self.assertEqual(
            [[1]],
            list(utils.chunk_list([1], 7))
        )
        self.assertEqual(
            [['L', 'o', 'r'], ['e', 'm', ' '], ['I', 'p', 's'], ['u', 'm']],
            list(utils.chunk_list(list('Lorem Ipsum'), 3))
        )
