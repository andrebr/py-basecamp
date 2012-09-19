# -*- coding: utf-8 -*-
"""
======
People
======

Get and delete people. A typical JSON response for a person looks like:

::

    {
        "id": 8675309,
        "name": "Tommy",
        "email_address": "me@example.com",
        "avatar_url": "https://example.com/foo.jpg",
        "updated_at": "2012-03-22T16:56:48-05:00",
        "url": "https://basecamp.com/9/api/v1/people/8675309-tommy.json"
    },

This class is not meant to add/remove people from projects, or grant them
access to documents/etc. That's what access is for.


.. todo::

    Link to ``accesses`` class when it is complete.

See `the Basecamp API docs
<https://github.com/37signals/bcx-api/blob/master/sections/people.md>`_
on people for more info.


"""
import json
from .base import Basecamp
from .exceptions import BasecampAPIError


class Person(Basecamp):
    """
    Operations on People in a particular project
    """
    def fetch(self, person=None):
        """
        Get a person, or a list of people.
        """
        if not person:
            # get the list.
            self.endpoint = 'people.json'

        request = self.get(self.construct_url())

        if request.status_code == 200:
            return json.loads(request.content)

        raise BasecampAPIError()

    def remove(self, person):
        """
        Delete a person
        """
