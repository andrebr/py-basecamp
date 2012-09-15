# -*- coding: utf-8 -*-
"""
basecamp
--------

Basecamp is a wrapper around the Basecamp Next API and makes use
of the `Requests <https://github.com/kennethreitz/requests>`_ library
made by Kenneth Reitz.

Basic usage:

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
"""

VERSION = (0, 0, 1, 'alpha', 0)

def get_version(mode='short'):
    """
    Returns a PEP 386-compliant version number from VERSION.
    """
    assert len(VERSION) == 5
    assert VERSION[3] in ('alpha', 'beta', 'rc', 'final')

    major = VERSION[0]
    minor = VERSION[1]
    terinary = VERSION[2]

    ver = '{0}.{1}'.format(major, minor)

    if mode == 'short':
        if terinary != 0:
            ver = ver + '.{0}'.format(terinary)

        return ver

    if mode == 'full':
        if terinary != 0:
            ver = ver + '.{0}'.format(terinary)

        if VERSION[3] in ('alpha', 'beta'):
            ver = '{0}{1}'.format(ver, VERSION[3][0])

        if VERSION[4] != 0:
            ver = '{0}{1}'.format(ver, VERSION[4])

        return ver


__version__ = get_version()
__title__ = 'basecamp'
__author__ = 'Greg Aker, nGen Works'
