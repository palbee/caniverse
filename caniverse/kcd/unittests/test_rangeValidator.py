from unittest import TestCase
from ..validators import RangeValidator
from django.core.validators import ValidationError


class TestRangeValidator(TestCase):
    def test_just_below_range(self):
        """Check the case where the input is just out of range at the lower end."""
        validator = RangeValidator(10, 20)
        with self.assertRaises(ValidationError, msg='Failed to raise exception') as context:
            validator(9)
        self.assertEquals(context.exception.code, 'out_of_range', 'Incorrect code.')

    def test_just_above_range(self):
        """Check the case where the input is just out of range at the upper end."""
        validator = RangeValidator(10, 20)
        with self.assertRaises(ValidationError, msg='Failed to raise exception') as context:
            validator(21)
        self.assertEquals(context.exception.code, 'out_of_range', 'Incorrect code.')

    def test_below_range(self):
        """Check the case where the input is    out of range at the lower end."""
        validator = RangeValidator(10, 20)
        with self.assertRaises(ValidationError, msg='Failed to raise exception') as context:
            validator(0)
        self.assertEquals(context.exception.code, 'out_of_range', 'Incorrect code.')

    def test_top_of_range(self):
        """Check the case where the input is in range at the upper end."""
        validator = RangeValidator(10, 20)
        self.assertIsNone(validator(20), msg='Should succeed silently')

    def test_bottom_of_range(self):
        """Check the case where the input is in range at the lower end."""
        validator = RangeValidator(10, 20)
        self.assertIsNone(validator(10), msg='Should succeed silently')

    def test_middle_of_range(self):
        """Check the case where the input is in middle of range."""
        validator = RangeValidator(10, 20)
        self.assertIsNone(validator(15), msg='Should succeed silently')

    def test_middle_of_range_reversed(self):
        """Check the case where the input is in middle of range."""
        validator = RangeValidator(20, 10)
        self.assertIsNone(validator(15), msg='Should succeed silently')

    def test_equality_of_validators(self):
        """Check that == returns true when it should"""
        validator = RangeValidator(10, 20)
        validator_other = RangeValidator(10, 20)
        self.assertEquals(validator, validator_other, msg='Validators should be the same.')

    def test_inequality_of_validators(self):
        validator = RangeValidator(10, 20)
        self.assertNotEquals(validator, RangeValidator(10, 21), msg='Validators should be different.')
        self.assertNotEquals(validator, RangeValidator(11, 20), msg='Validators should be different.')
        self.assertNotEquals(validator, RangeValidator(10, 20, message='%(lower)s <= %(value)s <= %(upper)s'),
                             msg='Validators should be different.')
        self.assertNotEquals(validator, RangeValidator(10, 20, code='code'),
                             msg='Validators should be different.')
        self.assertNotEquals(validator, 'other', msg='Validators should be different.')


