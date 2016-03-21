"""View for listing prices"""
from ..renderers.PriceChartPNGRenderer import PriceChartPNGRenderer
from ..serializers.PriceSerializer import PriceSerializer
from ...models.Price import Price

from datetime import timedelta

from django.utils import timezone

from rest_framework.generics import ListAPIView


class PriceListView(ListAPIView):
    model = Price
    serializer_class = PriceSerializer
    renderer_classes = ListAPIView.renderer_classes + [PriceChartPNGRenderer]

    def get_queryset(self):
        """
        Returns the elements matching the product's ASIN within the last 7 days.
        :return: QuerySet
        """
        # FIXME this has room fro improvement, we could only show the values that changes within a wider time range - but currently I don't know how to do that
        return self.model.objects.filter(
            product__asin=self.kwargs.get('asin'),
            date_seen__gte=timezone.now() - timedelta(days=7),
        ).order_by('-date_seen')
