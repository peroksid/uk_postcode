import logging

import unittest

from nose_parameterized import parameterized


from uk_postcode import decode


logging.basicConfig(level=logging.DEBUG)



class HappyWiki(unittest.TestCase):
    @parameterized.expand([
        ('DN55 1PT', {'SECTOR': 'DN55 1', 'TOWN': '55', 'AREA': 'DN', 'INWARD': '1PT', 'OUTWARD': 'DN55', 'UNIT': 'PT'}),
        ('CR2 6XH', {'SECTOR': 'CR2 6', 'TOWN': '2', 'AREA': 'CR', 'INWARD': '6XH', 'OUTWARD': 'CR2', 'UNIT': 'XH'}),
        ('B33 8TH', {'SECTOR': 'B33 8', 'TOWN': '33', 'AREA': 'B', 'INWARD': '8TH', 'OUTWARD': 'B33', 'UNIT': 'TH'}),
        ('M1 1AE', {'SECTOR': 'M1 1', 'TOWN': '1', 'AREA': 'M', 'INWARD': '1AE', 'OUTWARD': 'M1', 'UNIT': 'AE'}),
        ('W1A 0AX', {'SECTOR': 'W1A 0', 'TOWN': '1', 'AREA': 'W', 'INWARD': '0AX', 'OUTWARD': 'W1A', 'UNIT': 'AX'}),
        ('EC1A 1BB', {'SECTOR': 'EC1A 1', 'TOWN': '1', 'AREA': 'EC', 'INWARD': '1BB', 'OUTWARD': 'EC1A', 'UNIT': 'BB'})
    ])
    def test_codes(self, code, expected):
        self.assertEqual(decode(code), expected)
