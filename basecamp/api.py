"""
Basecamp API
"""
import json
import requests


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

    # pylint: disable=R0201,E1103
    def _do_request(self, url, **kwargs):
        """
        Perform the request.

        If post_args is passed as a keyword argument, assume that
        it is a POST request.
        """
        if kwargs.get('post_data'):
            # it's a post
            req = requests.post(url, data=kwargs['post_data'])
        else:
            if kwargs.get('headers'):
                req = requests.get(url, headers=kwargs['headers'])
            else:
                req = requests.get(url)

        if req.status_code != 200:
            raise BasecampAPIError(req.content)

        return req
