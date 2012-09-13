"""
Basecamp Auth tests
"""

import unittest
import basecamp


class AuthTests(unittest.TestCase):
    """
    Test the BasecampAuth class.
    """

    client_id = '12345asdfg'
    client_secret = '764332asvi44'
    return_url = 'http://127.0.0.1:8000/auth-return/'

    def test_get_launchpad_url(self):
        """
        Test creating the launchpad url.
        """
        auth = basecamp.BasecampAuth(
            self.client_id, self.client_secret, self.return_url)

        # pylint: disable=C0301
        self.assertEquals(auth.launchpad_url,
            'https://launchpad.37signals.com/authorization/new?redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fauth-return%2F&type=web_server&client_id=12345asdfg')
