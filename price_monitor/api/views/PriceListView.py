from ..renderers.PriceChartPNGRenderer import PriceChartPNGRenderer
from ..serializers.PriceSerializer import PriceSerializer
from ...models.Price import Price

from rest_framework.generics import ListAPIView


class PriceListView(ListAPIView):
    model = Price
    serializer_class = PriceSerializer
    renderer_classes = ListAPIView.renderer_classes + [PriceChartPNGRenderer]

    def get_queryset(self):
        queryset = super(PriceListView, self).get_queryset()
        # TODO: this is just for testing
        return queryset.filter(product__asin=self.kwargs.get('asin')).order_by('-date_seen')[:50]
