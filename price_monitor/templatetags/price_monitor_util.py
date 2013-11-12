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
