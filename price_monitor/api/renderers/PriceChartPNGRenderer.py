import dateutil.parser
import hashlib

from ... import app_settings

from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError

from pygal import DateTimeLine
from pygal.style import RedBlueStyle

from rest_framework.renderers import BaseRenderer

from tempfile import TemporaryFile


def bool_helper(x):
    return x in [1, '1', 'true', 'True']


class PriceChartPNGRenderer(BaseRenderer):
    """
    A renderer to render charts as PNG for prices
    """

    media_type = 'image/*'
    format = 'png'
    charset = None
    render_style = 'binary'

    # TODO: documentation
    allowed_chart_url_args = {
        'height': lambda x: int(x),
        'width': lambda x: int(x),
        'margin': lambda x: int(x),
        'no_data_font_size': lambda x: int(x),
        'spacing': lambda x: int(x),
        'show_dots': bool_helper,
        'show_legend': bool_helper,
        'show_x_labels': bool_helper,
        'show_y_labels': bool_helper,
        'show_minor_y_labels': bool_helper,
        'y_labels_major_count': lambda x: int(x),
    }

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        # first get the cache to use or None
        try:
            cache = caches[app_settings.PRICE_MONITOR_GRAPH_CACHE_NAME]
        except InvalidCacheBackendError:
            cache = None
        # sanitize arguments
        sanitized_args = self.sanitize_allowed_args(renderer_context['request']) if 'request' in renderer_context else {}

        # generate cache key
        cache_key = self.create_cache_key(data, sanitized_args)
        # only read from cache if there is any
        content = cache.get(cache_key) if cache is not None else None
        if content is None:
            # create graph instance
            graph = self.create_graph(data, sanitized_args)

            # write graph to temporary file
            with TemporaryFile() as file_:
                graph.render_to_png(file_)

                # only write to cache if there is any
                if cache is not None:
                    # seek back to start
                    file_.seek(0)
                    cache.set(cache_key, file_.read())
                # and back to start again
                file_.seek(0)
                # return the content
                return file_.read()
        else:
            # return the cache content
            return content

    def sanitize_allowed_args(self, request):
        """
        TODO: documentation
        """
        sanitized_args = {}
        if request.method == 'POST':
            args = request.POST
        elif request.method == 'GET':
            args = request.GET
        else:
            return sanitized_args

        for arg, sanitizer in self.allowed_chart_url_args.items():
            if arg in args:
                try:
                    sanitized_args[arg] = sanitizer(args[arg])
                except ValueError:
                    # sanitation gone wrong, so pass
                    pass
        return sanitized_args

    def create_cache_key(self, data, args):
        """
        Creates a cache key based on rendering data
        """
        hash_data = str(data['results']).encode('utf-8')
        hash_data += str(args).encode('utf-8')
        return app_settings.PRICE_MONITOR_GRAPH_CACHE_KEY_PREFIX + hashlib.md5(hash_data).hexdigest()

    def create_graph(self, data, args):
        """
        Creates the graph based on rendering data
        """
        line_chart_arguments = {
            'style': RedBlueStyle,
            'x_label_rotation': 25,
            'x_value_formatter': lambda dt: dt.strftime('%y-%m-%d %H:%M'),
        }
        for arg in self.allowed_chart_url_args.keys():
            if arg in args:
                line_chart_arguments.update({arg: args[arg]})

        line_chart = DateTimeLine(**line_chart_arguments)
        if 'results' in data and len(data['results']) > 0:
            values = [(dateutil.parser.parse(price['date_seen']), price['value']) for price in data['results']]
            line_chart.add(data['results'][0]['currency'], values)
        return line_chart
