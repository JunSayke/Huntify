import pprint

from django import template
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
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


@register.simple_tag
def call_method(model_path, method_name, *args):
    """
    Calls a method on a Django model class dynamically.

    Args:
        model_path (str): The dotted path to the model in the format 'app_name.ModelName'.
        method_name (str): The name of the method to call on the model class.
        *args: Additional arguments to pass to the method.

    Raises:
        ObjectDoesNotExist: If the model specified by model_path does not exist.
        AttributeError: If the method specified by method_name does not exist on the model class.
        TypeError: If the method specified by method_name is not callable.

    Returns:
        The result of the method call.
    """
    try:
        app_name, model_name = model_path.split('.')
        model_class = apps.get_model(app_name, model_name)
    except (LookupError, ValueError):
        raise ObjectDoesNotExist(f"Model '{model_path}' does not exist.")

    if not hasattr(model_class, method_name):
        raise AttributeError(f"{model_class} does not have method {method_name}")

    method = getattr(model_class, method_name)

    if not callable(method):
        raise TypeError(f"{method_name} is not callable on {model_class}")

    return method(*args)
