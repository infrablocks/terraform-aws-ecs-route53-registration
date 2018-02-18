import unittest

from ecs_route53_registration import validations


class TestValidations(unittest.TestCase):
    def test_returns_value_when_value_present(self):
        self.assertEqual(
            validations.ensure_present(
                'some-value',
                'Some configuration parameter must be provided.'),
            'some-value')

    def test_raises_value_error_when_value_is_empty_string(self):
        with self.assertRaisesRegex(
                ValueError,
                r"^Some configuration parameter must be provided\.$"):
            validations.ensure_present(
                '',
                'Some configuration parameter must be provided.')

    def test_raises_value_error_when_value_is_none(self):
        with self.assertRaisesRegex(
                ValueError,
                r"^Some configuration parameter must be provided\.$"):
            validations.ensure_present(
                None,
                'Some configuration parameter must be provided.')

    def test_returns_value_when_in_provided_set(self):
        self.assertEqual(
            validations.ensure_one_of(
                ['first', 'second'],
                'first',
                'Some configuration parameter must be one of: %s'),
            'first')

    def test_raises_value_error_when_value_is_not_in_set(self):
        with self.assertRaisesRegex(
                ValueError,
                r"^Some configuration parameter must be one of: "
                r"\[\'first\', \'second\'\]\.$"):
            validations.ensure_one_of(
                ['first', 'second'],
                'other',
                'Some configuration parameter must be one of: %s.')
