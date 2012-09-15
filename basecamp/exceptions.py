# -*- coding: utf-8 -*-
""" Exceptions """


class BasecampAPIError(Exception):
    """
    An issue with an API Call
    """
    pass


class ImproperlyConfigured(RuntimeError):
    """
    Some kind of issue setting up the API call.
    """
    pass
