"""
Tests for people actions.
"""

import json
import fudge
import unittest
import basecamp.api

from nose.tools import raises

from .base import BasecampBaseTest
from basecamp.exceptions import BasecampAPIError


class People(BasecampBaseTest):
    """
    People tests.
    """

    url = 'https://example.com/123/api/v1'
    token = 'JVGltZQ2WIxzA4/w4kg==--8f2687d'
    refresh_token = 'Apw45kg==--ae58c0e1dd82971660'

    response = [{
            "id": 149087659,
            "name": "Jason Fried",
            "email_address": "jason@37signals.com",
            "avatar_url": "https://avatar.96.gif?r=3",
            "updated_at": "2012-03-22T16:56:48-05:00",
            "url": "https://basecamp.com/1/api/v1/people/149087659-test.json"
        }, {
            "id": 1071630348,
            "name": "Jeremy Kemper",
            "email_address": "jeremy@37signals.com",
            "avatar_url": "https://asset0.37img.com/g/avatar.96.gif",
            "updated_at": "2012-03-22T16:56:48-05:00",
            "url": "https://basecamp.com/1/api/v1/people/1071630348-test.json"
        }]

    def setUp(self):
        super(People, self).setUp()

        self.people = basecamp.api.Person(
            self.url, self.token, self.refresh_token)

    def test_fetch_people_list(self):
        """
        Test fetching a list of people.
        """
        with fudge.patch('basecamp.base.Base.get') as fake_get:
            fake_get.is_callable().returns(
                self.setup_mock(200, self.response))

            self.assertEquals(self.people.fetch(), self.response)

    @raises(BasecampAPIError)
    def test_fetch_people_list_no_permission(self):
        """
        Ensure an exception is raised when someone does not have permission to
        view the people list.
        """

        with fudge.patch('basecamp.base.Base.get') as fake_get:
            fake_get.is_callable().returns(
                self.setup_mock(403, self.response))

            self.assertEquals(self.people.fetch(), self.response)

    def test_fetch_single_person(self):
        """
        Test fetching a single person.
        """
        with fudge.patch('basecamp.base.Base.get') as fake_get:
            fake_get.is_callable().returns(
                self.setup_mock(200, self.response[0]))

            self.assertEquals(
                self.people.fetch(person='me'), self.response[0])
