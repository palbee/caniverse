from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_bit_length(value):
    """Ensure that value is in the interval [1,64]."""
    if 1 <= value <= 64:
        raise ValidationError(
            _('%(value)s is outside of interval [1,64]'),
            params={'value': value},
        )