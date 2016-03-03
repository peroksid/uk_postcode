import unittest

from nose_parameterized import parameterized


from uk_postcode import decode


class HappyWiki(unittest.TestCase):
    @parameterized.expand([
        ('DN55 1PT', {'SECTOR': 'DN55 1', 'TOWN': '55', 'AREA': 'DN', 'INWARD': '1P', 'OUTWARD': 'DN55', 'UNIT': 'P'})
    ])
    def test_codes(self, code, expected):
        self.assertEqual(decode(code), expected)
