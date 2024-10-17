from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def conditional_class(class_name):
    """
    Adds a class attribute to an HTML element if the class_name is provided.
    Usage: {% conditional_class "your-class-name" %}
    """
    if class_name:
        result = f'class="{class_name}"'
        return mark_safe(result)
    return ''

@register.filter
def insert_field_attrs(field, exclude=None):
    """
    Inserts HTML attributes into a form field based on its widget attributes.
    Optionally excludes specified attributes.

    Usage: {{ form.field|insert_field_attrs:"attr1,attr2" }}

    Args:
        field: The form field to which attributes will be added.
        exclude: A comma-separated string of attribute names to exclude.

    Returns:
        A string of HTML attributes to be inserted into the form field.
    """
    exclude = [] if exclude is None else exclude.split(',')

    attrs = [
        f'{attr}="{value}"' for attr, value in field.field.widget.attrs.items()
        if attr not in exclude
    ]
    if 'required' not in exclude and field.field.required:
        attrs.append('required')
    if 'autofocus' not in exclude and field.field.widget.attrs.get('autofocus'):
        attrs.append('autofocus')
    if 'maxlength' not in exclude and field.field.widget.attrs.get('maxlength'):
        attrs.append(f'maxlength="{field.field.widget.attrs["maxlength"]}"')
    return mark_safe(' '.join(attrs))
