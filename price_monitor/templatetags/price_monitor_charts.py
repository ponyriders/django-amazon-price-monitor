from django import template
from django.conf import settings
from django.template.loader import render_to_string

from random import randint

register = template.Library()


@register.simple_tag
def charts_load_js_amd_css(*args):
    # TODO docu
    css_files = [
        'nv.d3.css',
    ]

    js_files = [
        'd3.v2.min.js',
        'nv.d3.min.js',
    ]

    if 'line' in args:
        js_files += ['line.js', 'lineChart.js', ]

    html = ''

    for css in css_files:
        html += '<link href="%(static_url)sprice_monitor/nvd3/css/%(file)s" rel="stylesheet" type="text/css">' % {
            'static_url': settings.STATIC_URL,
            'file': css
        }

    for js in js_files:
        html += '<script src="%(static_url)sprice_monitor/nvd3/js/%(js)s"></script>' % {'static_url': settings.STATIC_URL, 'js': js}

    return html


@register.simple_tag
def chart_line(width, height, data, show_yaxis, title, color):
    # TODO css separieren
    # TODO js auslagern sofern mgl.
    # TODO bei tooltip datum anzeigen -> formatieren
    # TODO minimize
    # TODO docu
    return render_to_string(
        'price_monitor/templatetags/chart_line.html',
        {
            'color': color,
            'data': data,
            'id': randint(0, 1000000000),
            'height': height,
            'show_yaxis': True if show_yaxis == 1 else False,
            'title': title,
            'width': width,
        },
    )