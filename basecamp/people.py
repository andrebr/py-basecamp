# -*- coding: utf-8 -*-
"""
People class

https://github.com/37signals/bcx-api/blob/master/sections/people.md
"""
from .api import Base


class People(Base):
    """
    Operations on People in the API
    """
    def fetch(self, person=None):
        """
        Get a person, or a list of people.
        """

    def delete(self, person):
        """
        Delete a person
        """
