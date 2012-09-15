# -*- coding: utf-8 -*-
"""
basecamp
------------

This module exists in order to do * imports from.

If this was handled in __init__, there would be issues with
getting the version and handling dependencies in setup.py.
"""

from .auth import Auth
from .base import Basecamp
