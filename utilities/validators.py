import re
from django.core.exceptions import ValidationError


def validate_philippines_phone_number(value):
    pattern = re.compile(r'^09[0-9]{9}$')
    if not pattern.match(value):
        raise ValidationError('Enter a valid Philippines phone number starting with 09 followed by 9 digits.')
