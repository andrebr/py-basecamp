# -*- coding: utf-8 -*-
"""
====================
Basecamp API Wrapper
====================

Basecamp is a wrapper around the
`Basecamp Next API <https://github.com/37signals/bcx-api>`_ and makes use
of the `Requests <https://github.com/kennethreitz/requests>`_ library
made by Kenneth Reitz.

The py-basecamp source code is hosted on GitHub:
https://github.com/ngenworks/py-basecamp/

Test coverage results can be found at
https://secure.travis-ci.org/#!/ngenworks/py-basecamp


Automatic Installation
----------------------

Install the master branch from GitHub

::

    pip -e git+git://github.com/ngenworks/py-basecamp.git#egg=basecamp


Manual Installation
-------------------

Download: https://github.com/ngenworks/py-basecamp/tarball/master

::

    tar zxvf py-basecamp.tgz
    cd py-basecamp
    python setup.py install

sudo may be needed to install in the system-wide Python installation.
Using in a `virtualenv <http://www.virtualenv.org/>`_ is recommended.
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
