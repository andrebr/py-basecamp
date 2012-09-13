"""
Basecamp Auth tests
"""
import fudge
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

    @fudge.patch('basecamp.BasecampAuth.get_token')
    def test_get_token(self, get_token):
        """
        Test getting the token from a request.
        """
        return_data = {
            "expires_in":1209600,
            "refresh_token":"BAhb7ImV4cGlyZXNfY7gkkdnKXQiOiIyMDIyLTA5L"
                "TEzVDA0OjU5OjIxWiIsInVzZXJfaWRzIjpbMjk4OTM3Nyw5Njg4Mj"
                "ZDA1N2AAhjsadfOIuylasdfVAJsmMWZhMTFiYiJ9dToJVGltZQ2ko"
                "R7AmMFd7Q==--e94437b619d869",
            "access_token":"BAhbByICSwF767sALaksdtamYXQiOiIyMDEyLTA5LT"
                "I3VDA0OjU5OjIxWiIsInVzZXJfaWRzIjpbMjk4OTM3Nyw5Njg4MjI"
                "yLDk2NjcwMzgsMTAzNTEzNzAsMTE4MDAxODAsNDE2ODg0MCw2NDU0"
                "DA1N2ZjMDoKsadFAkljasdfLKjdMWZhMTFiYiJ9dToJVGltZQ1kIx"
                "zA7bBd7Q==--9dcc4400b03"
        }

        auth = basecamp.BasecampAuth(
            self.client_id, self.client_secret, self.return_url)
        mock_token = auth.get_token\
            .expects_call()\
            .returns(return_data)

        token = get_token('123456p')

        self.assertEquals(
            token.get('access_token'),
            return_data['access_token']
        )

    @fudge.patch('basecamp.BasecampAuth.get_token')
    def test_expired_token(self, get_token):
        """
        Test an expired token.
        """
        return_data = {
            "error": "expired_verification_code"
        }

        auth = basecamp.BasecampAuth(
            self.client_id, self.client_secret, self.return_url)
        mock_token = auth.get_token\
            .expects_call()\
            .returns(return_data)

        token = get_token('thisisbad')


