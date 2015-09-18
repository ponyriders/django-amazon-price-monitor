from django.test import TestCase

from price_monitor import utils

from testfixtures import log_capture


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

    def test_chunk_list(self):
        """
        Tests the chunk_list function
        """
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
