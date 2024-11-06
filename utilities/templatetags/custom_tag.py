import pprint
from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.filter
def pprint_dir(obj):
    return pprint.pformat(dir(obj))


@register.simple_tag(takes_context=True)
def include_once(context, template_name):
    if 'included_templates' not in context.dicts[0]:
        context.dicts[0]['included_templates'] = set()

    if template_name not in context.dicts[0]['included_templates']:
        context.dicts[0]['included_templates'].add(template_name)
        return render_to_string(template_name, context.flatten())
    else:
        return ""
