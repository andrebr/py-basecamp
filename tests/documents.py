"""
Tests for documents actions.
"""

import json
import fudge
import unittest
import basecamp.api

from nose.tools import raises

from .base import BasecampBaseTest
from basecamp.exceptions import BasecampAPIError


class Documents(BasecampBaseTest):
    """
    Documents tests.
    """
    url = 'https://example.com/123/api/v1'
    token = 'JVGltZQ2WIxzA4/w4kg==--8f2687d'
    refresh_token = 'Apw45kg==--ae58c0e1dd82971660'

    documents_list = [{
        'id': 1,
        'project_id': 1,
        'name': 'Have you heard the news?',
        'text': 'Giant Steps in Giant Shoes.'
    },
    {
        'id': 2,
        'project_id': 2,
        'name': 'If you miss the A train',
        'text': 'You\'ll find you missed the quickest way to Harlem'
    }]

    def setUp(self):
        super(Documents, self).setUp()

        self.document = basecamp.api.Document(
            self.url, self.token, self.refresh_token)

    def test_fetch(self):
        """
        Test fetching a list of documents.
        """
        with fudge.patch('basecamp.base.Base.get') as fake_get:

            # Get all the documents.
            mock = self.setup_mock(200, self.documents_list)
            fake_get.is_callable().returns(mock)

            self.assertEqual(self.document.fetch(), self.documents_list)

            # Get documents for a single project
            mock = self.setup_mock(200, self.documents_list)
            fake_get.is_callable().returns(mock)
            self.assertEqual(
                self.document.fetch(project_id=1), self.documents_list)

            # Get a specific document from a project
            mock = self.setup_mock(200, self.documents_list[0])
            fake_get.is_callable().returns(mock)

            self.assertEqual(
                self.document.fetch(project_id=1, document_id=1),
                self.documents_list[0])

    @raises(BasecampAPIError)
    def test_fetch_document_but_no_project(self):
        """
        Ensure an exception is thrown if `document_id` is passed to `fetch()`
        but no `project_id` is included
        """
        self.document.fetch(document_id=1)

    @raises(BasecampAPIError)
    def test_fetch_test_404(self):
        """
        Test what happens when a 404 is returned.
        """
        with fudge.patch('basecamp.base.Base.get') as fake_get:
            mock = self.setup_mock(404)
            fake_get.is_callable().returns(mock)

            self.document.fetch(project_id=1, document_id=1)

    def test_create_document(self):
        """
        Test creating a new document.
        """
        response = {
            'id': 8675309,
            'project_id': 66,
            'name': 'Jenny',
            'content': 'I got it!<br>I got it!'
        }

        with fudge.patch('basecamp.base.Base.post') as fake_post:
            fake_post.is_callable().returns(self.setup_mock(201, response))

            self.assertEqual(
                self.document.create(66, 'Jenny', 'I got it!<br>I got it!'),
                response)

    @raises(BasecampAPIError)
    def test_create_document_no_permission(self):
        """
        Test creating a new document.
        """
        with fudge.patch('basecamp.base.Base.post') as fake_post:
            fake_post.is_callable().returns(self.setup_mock(403))
            self.document.create(66, 'Jenny', 'I got it!<br>I got it!')

    @raises(BasecampAPIError)
    def test_create_odd_status_code(self):
        """
        Test updating a document but dealing with a 403 response
        """
        response = {
            'title': 'foobar',
            'content': 'baz'
        }

        with fudge.patch('basecamp.base.Base.post') as fake_put:
            fake_put.is_callable().returns(self.setup_mock(501, response))
            self.assertEqual(self.document.create(66, 'foobar', 'baz'),
                response)

    def test_update_document(self):
        """
        Test updating a document.
        """
        response = {
            'title': 'foobar',
            'content': 'baz'
        }

        with fudge.patch('basecamp.base.Base.put') as fake_put:
            fake_put.is_callable().returns(self.setup_mock(200, response))
            self.assertEqual(self.document.update(1, 2, 'foobar', 'baz'),
                response)

    @raises(BasecampAPIError)
    def test_update_document(self):
        """
        Test updating a document but dealing with a 403 response
        """
        response = {
            'title': 'foobar',
            'content': 'baz'
        }

        with fudge.patch('basecamp.base.Base.put') as fake_put:
            fake_put.is_callable().returns(self.setup_mock(403, response))
            self.assertEqual(self.document.update(1, 2, 'foobar', 'baz'),
                response)

    def test_remove_document(self):
        """
        Test removing a document.
        """
        with fudge.patch('basecamp.base.Base.delete') as fake_del:
            fake_del.is_callable().returns(self.setup_mock(204))
            self.assertTrue(self.document.remove(1, 1))

