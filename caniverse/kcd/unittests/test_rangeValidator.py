from unittest import TestCase
from ..validators import RangeValidator
from django.core.validators import ValidationError

class TestRangeValidator(TestCase):
    def test_below_range(self):
        validator = RangeValidator(10, 20)
        with self.assertRaises(ValidationError, msg='Failed to raise exception'):
            validator(9)
