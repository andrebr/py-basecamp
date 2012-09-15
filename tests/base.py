"""
Test Base.
"""
import unittest

from nose.tools import raises

from basecamp.api import Basecamp
from basecamp.exceptions import ImproperlyConfigured


# pylint: disable=R0903
class RequestMock(object):
    """
    A mock request class.
    """
    status_code = None
    content = None


class BuildURLTests(unittest.TestCase):
    """
    Test that the URL builder is building correct urls.
    """

    # pylint: disable=R0201
    @raises(ImproperlyConfigured)
    def test_no_endpoint(self):
        """
        Test what happens if the endpoint class attr isn't set.
        """
        account_url = 'http://example.com'
        access_token = 'abceasyas123'

        some_api = Basecamp(account_url, access_token)
        some_api.construct_url()

    def test_good_url(self):
        """
        Test construction of a URL.
        """
        account_url = 'http://example.com'
        access_token = 'abceasyas123'

        some_api = Basecamp(account_url, access_token)
        some_api.endpoint = 'foobars'
        self.assertEquals(
            some_api.construct_url(),
            'http://example.com/foobars?access_token=abceasyas123')

    def test_endpoint_slashes(self):
        """
        Test that slashes are removed from the endpoint.
        """
        account_url = 'http://example.com'
        access_token = 'abceasyas123'

        some_api = Basecamp(account_url, access_token)
        some_api.endpoint = '/foobars/'
        self.assertEquals(
            some_api.construct_url(),
            'http://example.com/foobars?access_token=abceasyas123')
