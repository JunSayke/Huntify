import pprint
from django import template

register = template.Library()


@register.filter
def pprint_dir(obj):
    return pprint.pformat(dir(obj))
