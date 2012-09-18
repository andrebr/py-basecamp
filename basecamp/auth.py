# -*- coding: utf-8 -*-
"""
====
Auth
====

The Basecamp API follows draft 5 of the `oAuth 2 spec
<http://tools.ietf.org/html/draft-ietf-oauth-v2>`_

In short, this is how it works:

* Ask for access
* A user authenticates with their Basecamp account
* Get a verification code.
* Trade that code in for an access token.
* Start performing authenticated requests with said token.

-----------
Basic usage
-----------

    >>> import basecamp.api
    >>> auth = basecamp.api.Auth(client_url, client_secret, redirect_url)
    >>> launchpad_url = auth.launchpad_url

Redirect to the ``launchpad_url`` in your application
after the user authenticates, they are redirected back to the
redirect_url location, and a `code` GET variable will be present
to exchange for a token.

    >>> import basecamp.api
    >>> auth = basecamp.api.Auth(client_url, client_secret, redirect_url)
    >>> token = auth.get_token()


--------
Examples
--------

Here's a basic example of how this could work in a Flask application.

::

    import basecamp.api
    from secrets import client_id, client_secret, return_url
    from flask import Flask, redirect, request

    app = Flask(__name__)

    @app.route('/basecamp-login/')
    def basecamp_login():
        '''
        Redirect user to basecamp to authenticate.
        '''
        auth = basecamp.api.Auth(client_id, client_secret, return_url)

        return redirect(auth.launchpad_url)

    @app.route('/auth-return/')
    def auth_return():
        '''
        Get the code and exchange it for an access_token
        '''
        code = request.args.get('code')

        auth = basecamp.api.Auth(client_id, client_secret, return_url)

        token = auth.get_token(code)

        # do things now that you have a token.

"""
import urllib
import json

from .base import Base
from .exceptions import BasecampAPIError


class Auth(Base):
    """
    Class to perform basic auth operations
    """

    auth_type = 'web_server'
    auth_base_url = 'https://launchpad.37signals.com/'

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_secret = client_secret
        self.query_args = dict(
            client_id=client_id,
            type=self.auth_type,
            redirect_uri=redirect_uri
        )

        super(Auth, self).__init__()

    def __repr__(self):
        return '<BasecampAuth at 0x%x>' % (id(self))

    @property
    def launchpad_url(self):
        """
        Get the URL to send your application to.

        For instance, in a Django app, one could do something like:

        >>> import basecamp.api
        >>> from django import http
        >>> auth = basecamp.api.Auth(client_id, client_secret, redirect_uri)
        >>> http.HttpResponseRedirect(auth.get_launchpad_url)
        """
        return '{0}authorization/new?{1}'.format(
            self.auth_base_url,
            urllib.urlencode(self.query_args))

    def get_token(self, code):
        """
        This function requests the auth token from basecamp after
        oAuth has happened and the user has approved the application.

        :param code: the code returned from :meth:`launchpad_url`
        :rtype: dictionary

        The response should contain the following:

        - expires_in (seconds)
        - access_token (a really long string, you'll need this later)
        - refresh_token (another really long string. Hang onto this as well.)
        """
        self.query_args.update({
            'code': code,
            'client_secret': self.client_secret
        })
        url = '{0}authorization/token'.format(self.auth_base_url)
        request = self.post(url, post_data=self.query_args)

        if request.status_code == 200:
            return json.loads(request.content)  # pylint: disable=E1103

        raise BasecampAPIError(json.loads(request.content).get('error'))

    def _do_authorization_request(self, access_token):
        """
        Do the authorization request.

        This method is used by ``get_identity`` and ``get_accounts``
        """
        url = '{0}authorization.json'.format(self.auth_base_url)
        headers = {
            'Authorization': 'Bearer {0}'.format(access_token)
        }

        return self.get(url, headers=headers)

    def get_identity(self, access_token):
        """
        Get the users identity.

        As per the `docs <https://github.com/37signals/api/blob/master/\
        sections/authentication.md>`_:

            An identity is **NOT** used for determining who this user is
            within a specific application. The id field should NOT be used for
            submitting data within any application's API. This field can be
            used to get a user's name and email address quickly, and the id
            field could be used for caching on a cross-application basis if
            needed.

        :param access_token: access token obtained from :meth:`get_token`
        :rtype: dictionary
        """
        request = self._do_authorization_request(access_token)

        if request.status_code == 200:
            return request.content.get('identity')

        raise BasecampAPIError(json.loads(request.content).get('error'))

    def get_accounts(self, access_token, account_type='bcx'):
        """
        Get 37signals accounts for the authenticated user.

        :param access_token: access token obtained from :meth:`get_token`
        :param account_type: type of basecamp account to return. Return only \
            Basecamp Next accounts by default.
        :rtype: dictionary
        """
        request = self._do_authorization_request(access_token)

        if request.status_code == 200:
            if account_type == 'all':
                return json.loads(request.content.get('accounts'))
            else:
                _accounts = []

                for account in json.loads(request.content).get('accounts'):
                    if account['product'] == account_type:
                        _accounts.append(account)

                return _accounts

        raise BasecampAPIError(json.loads(request.content).get('error'))
