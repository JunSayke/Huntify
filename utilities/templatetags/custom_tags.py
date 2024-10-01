from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def conditional_class(class_name):
    if class_name:
        result = f'class="{class_name}"'
        return mark_safe(result)
    return ''

@register.inclusion_tag('forms/account_type_form.html')
def render_account_type_form(form):
    return {'form': form}