from django import template


register = template.Library()


@register.filter
def get(d, key):
    """
    Reads value from dictionary
    :value d: Dictionary to get value from
    :value key: The key to find
    :returns: Value for key
    """
    return d[key] if key in d else ''


@register.inclusion_tag('price_monitor/templatetags/pagination.html', takes_context=True)
def pagination(context):
    """
    Renders pagination template with full context
    :param context: Context of page
    :type  context: RequestContext
    :return:        Context
    :rtype:         RequestContext
    """
    return context
