# -*- coding: utf-8 -*-
import requests
import urllib
from .exceptions import (ImproperlyConfigured, BasecampAPIError)


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
        headers = {
            'Content-type': 'application/json; charset=utf-8'
        }

        if kwargs.get('post_data'):
            req = requests.post(url,
                data=kwargs['post_data'],
                headers=headers)
        else:
            if kwargs.get('headers'):
                headers.update(kwargs['headers'])
                req = requests.get(url, headers=headers)
            else:
                req = requests.get(url)

        if req.status_code == 500:
            raise BasecampAPIError('An unexpected error occurred.')
        elif req.status_code == 429:
            raise BasecampAPIError('Too many requests.')
        return req


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
        if not self.endpoint:
            raise ImproperlyConfigured('No endpoint has been set.')

        # strip slashes from the endpoint.
        self.endpoint = self.endpoint.strip('/')

        return '{0}/{1}?{2}'.format(
            self.account_url,
            self.endpoint,
            urllib.urlencode({'access_token': self.access_token})
        )
