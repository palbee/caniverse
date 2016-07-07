from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class RangeValidator(object):
    """Inspired by django.core.validators.BaseValidator"""
    message = _('Ensure this value is in the interval [%(lower)s, %(upper)s] (it is %(value)s).')
    code = 'out_of_range'

    def __init__(self, lower, upper, message=None, code=None):
        if lower <= upper:
            self.lower, self.upper = lower, upper
        else:
            self.lower, self.upper = upper, lower

        if message:
            self.message = message

        if code:
            self.code = code

    def __call__(self, value):
        if not self.lower <= value <= self.upper:
            params = {'lower': self.lower, 'upper': self.upper, 'value': value}
            raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            (self.lower == other.lower) and
            (self.upper == other.upper) and
            (self.message == other.message) and
            (self.code == other.code)
        )
