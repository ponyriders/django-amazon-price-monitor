from django import template
from django.conf import settings
from django.template.loader import render_to_string

from random import randint

register = template.Library()


@register.simple_tag
def charts_load_js_amd_css(*args):
    """
    Loads the javascript and stylesheets for the given chart types.
    :param args: list of chart types.
    :return: html string
    """
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
def chart_line(width, height, data, show_y_axis, title, color):
    """
    Creates a fancy line chart using NVD3.
    :param width: width of the chart as "500px"
    :param height: height of the chart as "300px"
    :param data: the data to be displayed. A list of dictionaries with x and y keys, e.g. [{x: 1, y:0}, {x:2, y:-1}]
    :param show_y_axis: if to show the y axis
    :param title: the title of the chart. Only used to separate if there are multiple charts.
    :param color: the color to draw the chart with
    :return: string with appropriate HTML
    """
    return render_to_string(
        'price_monitor/templatetags/chart_line.html',
        {
            'color': color,
            'data': data,
            'id': randint(0, 1000000000),
            'height': height,
            'show_y_axis': True if show_y_axis == 1 else False,
            'title': title,
            'width': width,
        },
    )