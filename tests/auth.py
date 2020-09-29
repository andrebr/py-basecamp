"""
Basecamp Auth tests
"""
import json
import fudge
import unittest
import basecamp.api

from nose.tools import raises

from .base import BasecampBaseTest
from basecamp.exceptions import BasecampAPIError


class Auth(BasecampBaseTest):
    """
    Test the Auth class.
    """

    client_id = '12345asdfg'
    client_secret = '764332asvi44'
    return_url = 'http://127.0.0.1:8000/auth-return/'

    # pylint: disable=C0103
    def setUp(self):
        super(Auth, self).setUp()
        self.auth = basecamp.api.Auth(
            self.client_id, self.client_secret, self.return_url)

    def test_get_launchpad_url(self):
        """
        Test creating the launchpad url.
        """

        # pylint: disable=C0301
        self.assertEqual(self.auth.launchpad_url,
            'https://launchpad.37signals.com/authorization/new?redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fauth-return%2F&type=web_server&client_id=12345asdfg')

    @raises(BasecampAPIError)
    def test_get_token_with_bad_code(self):
        """
        Test getting the token, but with a bad response.
        """
        with fudge.patch('basecamp.base.Base.post') as fake_post:
            mock = self.setup_mock(400, {
                'error': 'This verification code was already used. '
                         'Verification codes are single-use'})

            fake_post.is_callable().returns(mock)
            self.auth.get_token('foobar')

    def test_successful_token(self):
        """
        Get a good token.
        """

        content = {
            'access_token': 'abceasyas123==--1d3c',
            'expires_in': 1209600,
            'refresh_token': 'yICSwF7ImV4c==--zxvf'
        }

        with fudge.patch('basecamp.base.Base.post') as fake_post:
            fake_post.is_callable().returns(self.setup_mock(200, content))
            self.assertEqual(
                self.auth.get_token('foobar'),
                content)
