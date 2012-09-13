"""
Test get_version
"""
import unittest
import basecamp
from basecamp import get_version


class GetVersionTest(unittest.TestCase):
    """
    Tests getting the version.
    """

    versions = [
        (
            (0, 1, 0, 'alpha', 0),  # VERSION Tuple
            '0.1',  # short
            '0.1a',  # full
        ),
        (
            (0, 1, 1, 'beta', 1),  # VERSION tuple
            '0.1.1',  # short
            '0.1.1b1',  # full
        ),
    ]

    def test_short_version(self):
        """
        Testing short version, eg: 0.1, 0.1.1, etc.
        """
        for version in self.versions:
            basecamp.VERSION = version[0]
            self.assertEqual(
                get_version('short'), version[1])

    def test_full_version(self):
        """
        Test full version, eg: 0.1.1a1
        """
        for version in self.versions:
            basecamp.VERSION = version[0]
            self.assertEqual(
                get_version('full'), version[2])
