"""
Tests for projects actions.
"""

import json
import fudge
import unittest
import basecamp.api

from nose.tools import raises

from .base import RequestMock
from basecamp.exceptions import BasecampAPIError


class Projects(unittest.TestCase):
    """
    Projects tests.
    """

    url = 'https://example.com/123/api/v1'
    token = 'JVGltZQ2WIxzA4/w4kg==--8f2687d'
    refresh_token = 'Apw45kg==--ae58c0e1dd82971660'

    def test_list(self):
        """
        Get list of projects
        """

        response = [
            {
                "id": 605816632,
                "name": "BCX",
                "description": "The Next Generation",
                "updated_at": "2012-03-23T13:55:43-05:00",
                "url": "{0}/projects/605816632-bcx.json".format(self.url),
                "archived": False,
                "starred": True
            },
            {
                "id": 684146117,
                "name": "Nothing here!",
                "description": None,
                "updated_at": "2012-03-22T16:56:51-05:00",
                "url": "{0}/projects/684146117-nothing.json".format(self.url),
                "archived": False,
                "starred": False
            }
         ]

        with fudge.patch('basecamp.base.Base.get') as fake_get:
            mock = RequestMock
            mock.status_code = 200
            mock.content = json.dumps(response)

            fake_get.is_callable().returns(mock)

            projects = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            self.assertEquals(projects.fetch(), response)

    @raises(BasecampAPIError)
    def test_list_error(self):
        """
        Ensure an exception is thrown on a 404
        """
        # test a 404 error
        with fudge.patch('basecamp.base.Base.get') as fake_get:
            mock = RequestMock
            mock.status_code = 404
            mock.content = json.dumps({'error': 'something went wrong'})

            fake_get.is_callable().returns(mock)

            projects = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            projects.fetch()

    def test_create(self):
        """
        Create a project
        """
        response = {
            "id": 605816632,
            "name": "BCX",
            "description": "The Next Generation",
            "updated_at": "2012-03-23T13:55:43-05:00",
            "url": "{0}projects/605816632-bcx.json".format(self.url),
            "archived": False,
            "starred": True
        }

        with fudge.patch('basecamp.base.Base.post') as fake_post:
            mock = RequestMock
            mock.status_code = 201
            mock.content = json.dumps(response)

            fake_post.is_callable().returns(mock)

            project = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            new_project = project.create('Some Project', 'Project Description')

            self.assertEquals(new_project, response)

    @raises(BasecampAPIError)
    def test_create_no_permissions(self):
        """
        When a user does not have permission to create a project, an exception
        will be raised
        """

        with fudge.patch('basecamp.base.Base.post') as fake_post:
            mock = RequestMock
            mock.status_code = 403

            fake_post.is_callable().returns(mock)

            project = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            project.create('Some Project', 'Project Description')

    def test_detail(self):
        """
        Get project detail
        """

        response = {
            "archived": False,
            "documents": {
                "count": 0,
                "url": "{0}/projects/9-test/documents.json".format(self.url),
                "updated_at": None
            },
            "description": "Giant Steps",
            "forwards": {
                "count": 0,
                "url": "{0}/projects/9-test/forwards.json".format(self.url),
                "updated_at": None
            },
            "creator": {
                "avatar_url":
                    "http://asset0.37img.com/global/9f/avatar.gif?r=3",
                "id": 2440081,
                "name": "John Coltrane"
            },
            "created_at": "2012-09-14T22:50:03-05:00",
            "updated_at": "2012-09-15T00:24:26-05:00",
            "accesses": {
                "count": 1,
                "url": "{0}/projects/9-test/accesses.json".format(self.url),
                "updated_at": "2012-09-14T22:50:03-05:00"
            },
            "attachments": {
                "count": 0,
                "url": "{0}/projects/9-test/attachments.json".format(self.url),
                "updated_at": None
            },
            "todolists": {
                "url": "{0}/projects/9-test/todolists.json".format(self.url),
                "completed_count": 0,
                "updated_at": None,
                "remaining_count": 0
            },
            "calendar_events": {
                "count": 0,
                "url": "{0}/projects/9-test/calendar_events.json".format(
                    self.url),
                "updated_at": None
            },
            "topics": {
                "count": 0,
                "url": "{0}/projects/9-test/topics.json".format(self.url),
                "updated_at": None
            },
            "starred": False,
            "id": 9,
            "name": "test"
        }

        with fudge.patch('basecamp.base.Base.get') as fake_get:
            mock = RequestMock
            mock.status_code = 200
            mock.content = json.dumps(response)

            fake_get.is_callable().returns(mock)

            projects = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            self.assertEquals(projects.fetch(project=9), response)

    @raises(BasecampAPIError)
    def test_detail_error(self):
        """
        Ensure an exception is raised in the event the user does not have
        permissions to view the requested project's details.
        """

        response = {'error': 'no permission'}

        with fudge.patch('basecamp.base.Base.get') as fake_get:
            mock = RequestMock
            mock.status_code = 403
            mock.content = json.dumps(response)

            fake_get.is_callable().returns(mock)

            projects = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            projects.fetch(project=9)

    def test_edit(self):
        """
        Edit a project
        """

        response = {'id': 1, 'name': 'foobar', 'description': 'something'}

        with fudge.patch('basecamp.base.Base.put') as fake_put:
            mock = RequestMock
            mock.status_code = 200
            mock.content = json.dumps(response)

            fake_put.is_callable().returns(mock)

            project = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            self.assertEquals(project.update(1, 'foobar', 'something'),
                response)

    @raises(BasecampAPIError)
    def test_edit_no_permission(self):
        """
        Ensure an exception is raised in the event the currently authenticated
        user does not have permission to edit the name and description of the
        project.
        """

        with fudge.patch('basecamp.base.Base.put') as fake_put:
            mock = RequestMock
            mock.status_code = 403

            fake_put.is_callable().returns(mock)

            project = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            project.update(1, 'foobar', 'something')

    def test_archive(self):
        """
        Archive a project
        """
        response = {
            'id': 9,
            'name': 'test',
            'description': 'some test',
            "archived": True,
        }

        with fudge.patch('basecamp.base.Base.put') as fake_put:
            mock = RequestMock
            mock.status_code = 200
            mock.content = json.dumps(response)
            fake_put.is_callable().returns(mock)

            project = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            self.assertEquals(project.archive(9, archive=True), response)

    @raises(BasecampAPIError)
    def test_archive_but_not_archived(self):
        """
        Test archiving, but what happens if it is not archived.

        I'm sure sure if this is valid to test, but it might make sense.
        Regardless, here we go.
        """
        response = {
            'id': 9,
            'name': 'test',
            'description': 'some test',
            "archived": False,
        }

        with fudge.patch('basecamp.base.Base.put') as fake_put:
            mock = RequestMock
            mock.status_code = 200
            mock.content = json.dumps(response)
            fake_put.is_callable().returns(mock)

            project = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            project.archive(9, archive=True)

    @raises(BasecampAPIError)
    def test_archive_no_permissions(self):
        """
        Ensure an exception is rasied in when a user who does not have
        permission to archive a project tries to do so.
        """
        with fudge.patch('basecamp.base.Base.put') as fake_put:
            mock = RequestMock
            mock.status_code = 403
            fake_put.is_callable().returns(mock)

            project = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            self.assertEquals(project.archive(9, archive=True), response)

    def test_delete(self):
        """
        Delete a project
        """
        with fudge.patch('basecamp.base.Base.delete') as fake_delete:
            mock = RequestMock
            mock.status_code = 204
            fake_delete.is_callable().returns(mock)

            project = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            self.assertTrue(project.remove(9))

    @raises(BasecampAPIError)
    def test_delete_no_perissions(self):
        """
        Ensure an exception is raised when a user does not have permission to
        delete a project.
        """
        with fudge.patch('basecamp.base.Base.delete') as fake_delete:
            mock = RequestMock
            mock.status_code = 403
            fake_delete.is_callable().returns(mock)

            project = basecamp.api.Project(
                self.url, self.token, self.refresh_token)

            self.assertTrue(project.remove(9))
