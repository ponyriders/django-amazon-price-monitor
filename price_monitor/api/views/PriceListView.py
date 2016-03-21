"""View for listing prices"""
from ..renderers.PriceChartPNGRenderer import PriceChartPNGRenderer
from ..serializers.PriceSerializer import PriceSerializer
from ...models.Price import Price
from ...models.Product import Product
from ... import app_settings

from collections import namedtuple

from datetime import timedelta

from django.db import connection
from django.utils import timezone

from rest_framework.generics import ListAPIView


class PriceListView(ListAPIView):
    model = Price
    serializer_class = PriceSerializer
    renderer_classes = ListAPIView.renderer_classes + [PriceChartPNGRenderer]

    def get_queryset(self):
        """
        Returns the elements matching the product's ASIN within the last 7 days.

        :return: list
        """
        try:
            product = Product.objects.get(asin=self.kwargs.get('asin'))
        except Product.DoesNotExist:
            return []

        cursor = connection.cursor()
        # this query fetches for prices that are distinct from there previous value. The previous date and value is included.
        # I asked for this here: http://stackoverflow.com/q/36136063/364244
        # and the basic answer can be found here: http://fle.github.io/detect-value-changes-between-successive-lines-with-postgresql.html
        cursor.execute(
            'SELECT p1.id, p1.date_seen, p1.value, p1.prev_value, p1.prev_date_seen, p1.currency FROM ('
            'SELECT p2.id, p2.date_seen, p2.value, p2.currency, lead(p2.value) OVER (ORDER BY p2.date_seen DESC) as prev_value, '
            'lead(p2.date_seen) OVER (ORDER BY p2.date_seen DESC) as prev_date_seen FROM price_monitor_price p2 '
            'WHERE p2.product_id = %(product_id)s ORDER BY p2.date_seen DESC) as p1 '
            'WHERE p1.value IS DISTINCT FROM p1.prev_value AND p1.date_seen > %(date_limit)s ORDER BY p1.date_seen DESC;',
            {
                'date_limit': (timezone.now() - timedelta(days=app_settings.PRICE_MONITOR_GRAPH_LAST_DAYS)).strftime('%Y-%m-%d'),
                'product_id': product.pk,
            }
        )
        price_trojan = namedtuple('Price', ['date_seen', 'value', 'currency'])
        prices = []

        # TODO should insert a value for each day and check the y-axis label display; otherwise the values are not displayed evenly distributed
        for r in cursor.fetchall():
            # tuple indexes as selection with p1.xxx
            # the current price
            prices.append(price_trojan(date_seen=r[1], value=r[2], currency=r[5]))
            # the previous price
            if r[4] is not None:
                prices.append(price_trojan(date_seen=r[4], value=r[3], currency=r[5]))

        return prices
