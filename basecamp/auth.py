""" Auth """
import urllib
import json

from .api import Base
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

        auth = BasecampAuth(client_id, client_secret, redirect_uri)
        auth.get_launchpad_url()
        """
        return '{0}authorization/new?{1}'.format(
            self.auth_base_url,
            urllib.urlencode(self.query_args))

    def get_token(self, code):
        """
        This function requests the auth token from basecamp after
        oAuth has happened and the user has approved the application.

        :param code: the code returned from :method:`launchpad_url`

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

    def account_info(self, access_token):
        """
        Get account info on the currently authenticated user.
        """
        url = '{0}authorization.json'.format(self.auth_base_url)
        headers = {
            'Authorization': 'Bearer {0}'.format(access_token)
        }

        request = self.get(url, headers=headers)
        data = json.loads(request.content)  # pylint: disable=E1103

        return data
