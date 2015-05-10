from ..renderers.PriceChartPNGRenderer import PriceChartPNGRenderer
from ..serializers.PriceSerializer import PriceSerializer
from ...models.Price import Price

from rest_framework.generics import ListAPIView


class PriceListView(ListAPIView):
    model = Price
    serializer_class = PriceSerializer
    renderer_classes = ListAPIView.renderer_classes + [PriceChartPNGRenderer]

    def get_queryset(self):
        # TODO: this is just for testing
        return self.model.objects \
            .filter(product__asin=self.kwargs.get('asin')) \
            .select_related(
                'subscription_set__email_notification',
                'price_set'
            ) \
            .order_by('-date_seen')[:50]
