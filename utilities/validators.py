import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_philippines_phone_number(value):
    pattern = re.compile(r'^09[0-9]{9}$')
    if not pattern.match(value):
        raise ValidationError('Enter a valid Philippines phone number starting with 09 followed by 9 digits.')


philippine_phone_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message="Phone number must be entered in the format: '09XXXXXXXXX'. Up to 11 digits allowed."
)
