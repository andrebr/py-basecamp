"""
Basecamp API
"""
import requests
import urllib
from .exceptions import BasecampAPIError


class Base(object):
    """
    Base class that handles performing API calls.
    """

    def get(self, url, headers=None):
        """
        Perform a GET request.
        """
        return self._do_request(url, headers=headers)

    def post(self, url, post_data=None):
        """
        Perform a POST request.
        """
        return self._do_request(url, post_data=post_data)

    def put(self, url):
        """
        Perform a PUT request.
        """

    def delete(self, url):
        """
        Perform a DELETE request.
        """

    # pylint: disable=R0201,E1103
    def _do_request(self, url, **kwargs):
        """
        Perform the request.

        If post_args is passed as a keyword argument, assume that
        it is a POST request.
        """
        if kwargs.get('post_data'):
            # it's a post
            request = requests.post(url, data=kwargs['post_data'])
        else:
            if kwargs.get('headers'):
                request = requests.get(url, headers=kwargs['headers'])
            else:
                request = requests.get(url)

        if request.status_code == 404:
            raise BasecampAPIError('404')

        return request


class Basecamp(Base):

    endpoint = None

    def __init__(self, account_url, access_token, refresh_token=None):
        self.account_url = account_url
        self.access_token = access_token
        self.refresh_token = refresh_token

    def construct_url(self):
        """
        Construct a url with the account url, complete API endpoint and
        the access token as a query string.
        """
        return '{0}/{1}?{2}'.format(
            self.account_url,
            self.endpoint,
            urllib.urlencode({'access_token': self.access_token})
        )
