# -*- coding: utf-8 -*-
import requests
import urllib
from .exceptions import (ImproperlyConfigured, BasecampAPIError)


class Base(object):
    """
    Base class that handles performing API calls.
    """

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }

    def get(self, url, headers=None):
        """
        Perform a GET request.
        """
        if headers:
            self.headers.update(headers)
        request = requests.get(url, headers=self.headers)

        return self._check_response_code(request)

    def post(self, url, payload=None):
        """
        Perform a POST request.
        """
        request = requests.post(url,
            data=payload,
            headers=self.headers)

        return self._check_response_code(request)

    def put(self, url, payload=None):
        """
        Perform a PUT request.
        """
        request = requests.put(url,
            data=payload,
            headers=self.headers)

        return self._check_response_code(request)

    def delete(self, url, payload=None):
        """
        Perform a DELETE request.
        """
        request = requests.delete(url,
            data=payload,
            headers=self.headers)

        return self._check_response_code(request)

    def _check_response_code(self, request):
        """
        Perform some final processing on the request.
        """
        if request.status_code == 500:
            raise BasecampAPIError('An unexpected error occurred.')
        elif request.status_code == 429:
            raise BasecampAPIError('Too many requests.')
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
        if not self.endpoint:
            raise ImproperlyConfigured('No endpoint has been set.')

        # strip slashes from the endpoint.
        self.endpoint = self.endpoint.strip('/')

        return '{0}/{1}?{2}'.format(
            self.account_url,
            self.endpoint,
            urllib.urlencode({'access_token': self.access_token})
        )
