# -*- coding: utf-8 -*-
"""
=========
Documents
=========


For more information, please see the official Basecamp API documentation on
`documents <https://github.com/37signals/bcx-api/blob/master/sections/documents.md>`_
"""
import json
from .base import Basecamp
from .exceptions import BasecampAPIError


class Document(Basecamp):
    """
    Actions on a document
    """
    def fetch(self, document_id=None, project_id=None):
        """
        Get a specific document, or a list of documents, either by project, or
        all documents a user has access to in the basecamp account.

        :param document_id: integer of document
        :param project_id: integer of project
        :rtype dictionary: Dictionary of documents, or a single document.

        .. note::

            There are three methods of document retrieval.

            1. Global for the account. ``document_id`` and ``project_id``
               kwargs are omitted
            2. Documents limited to a specific project.
               The ``project_id`` kwargs is passed to the method call.
            3. Details on a specific document.
               The ``project_id`` and ``document_id`` kwargs are passed
               to the method call.

        .. warning::

            Passing a ``document_id`` but no ``project_id`` will cause a
            :class:`BasecampAPIError` exception to be raised.

        **Examples:**

        *All documents in the account:*

        >>> import basecamp.api
        >>> url = 'https://basecamp.com/1/api/v1'
        >>> token = 'foo'
        >>> refresh_token = 'bar'
        >>> documents = basecamp.api.Document(url, token, refresh_token)
        >>> documents.fetch()

        *Get documents within a project:*

        >>> import basecamp.api
        >>> url = 'https://basecamp.com/1/api/v1'
        >>> token = 'foo'
        >>> refresh_token = 'bar'
        >>> documents = basecamp.api.Document(url, token, refresh_token)
        >>> documents.fetch(project_id=123)

        *Get details on a single document:*

        >>> import basecamp.api
        >>> url = 'https://basecamp.com/1/api/v1'
        >>> token = 'foo'
        >>> refresh_token = 'bar'
        >>> documents = basecamp.api.Document(url, token, refresh_token)
        >>> documents.fetch(document_id=123, project_id=123)

        """
        if not document_id and not project_id:
            self.endpoint = 'documents.json'
        elif not document_id and project_id:
            self.endpoint = 'projects/{0}/documents.json'.format(project_id)
        elif document_id and project_id:
            self.endpoint = 'projects/{0}/documents/{1}.json'.format(
                project_id, document_id)
        else:
            raise BasecampAPIError()

        request = self.get(self.construct_url())

        if request.status_code == 200:
            return json.loads(request.content)

        raise BasecampAPIError(json.loads(request.content).get('error'))

    def create(self, project_id, title, content):
        """
        Create a new document.

        :param project_id: project id to create the document in.
        :param title: title of the document.
        :param content: content of the new document.
        :rtype dictionary: dictionary representation of the new document.

        >>> import basecamp.api
        >>> url = 'https://basecamp.com/1/api/v1'
        >>> token = 'foo'
        >>> refresh_token = 'bar'
        >>> documents = basecamp.api.Document(url, token, refresh_token)
        >>> documents.create(22, 'Cole Porter Songs', 'My favorite songs.')

        .. note::

            The JSON response will look similar to getting details of a
            document from :meth:`fetch`
        """

        self.endpoint = 'projects/{0}/documents.json'.format(project_id)

        data = dict(
            title=title,
            content=content
        )

        request = self.post(self.construct_url(),
            payload=json.dumps(data))
        if request.status_code == 201:
            return json.loads(request.content)
        elif request.status_code == 403:
            raise BasecampAPIError()

        raise BasecampAPIError()

    def update(self, project_id, document_id, title, content):
        """
        Update a document.

        :param project_id: integer of project id
        :param document_id: integer of document id
        :param title: string of title
        :param content: string of document content
        :rtype dictionary: Document information

        >>> import basecamp.api
        >>> url = 'https://basecamp.com/1/api/v1'
        >>> token = 'foo'
        >>> refresh_token = 'bar'
        >>> documents = basecamp.api.Document(url, token, refresh_token)
        >>> documents.update(22, 244, 'foo title', 'bar content')

        .. note::

            The JSON response will look similar to getting details of a
            document from :meth:`fetch`

        """
        self.endpoint = 'projects/{0}/documents/{1}.json'.format(
            project_id, document_id)

        data = dict(
            title=title,
            content=content
        )
        request = self.put(self.construct_url(),
            payload=json.dumps(data))

        if request.status_code == 200:
            return json.loads(request.content)

        raise BasecampAPIError()

    def remove(self, project_id, document_id):
        """
        Delete a document from the project/account

        :param project_id: integer of project id
        :param document_id: integer of document id to remove
        :rtype boolean: ``True`` if the document is removed.

        >>> import basecamp.api
        >>> url = 'https://basecamp.com/1/api/v1'
        >>> token = 'foo'
        >>> refresh_token = 'bar'
        >>> documents = basecamp.api.Document(url, token, refresh_token)
        >>> documents.remove(22, 244)

        .. note::

            If the document is not removed, or if a problem occurs, a
            :class::`BasecampAPIError` exception will be raised.

        """
        self.endpoint = 'projects/{0}/{1}.json'.format(
            project_id, document_id)

        request = self.delete(self.construct_url())

        if request.status_code == 204:
            return True

        return BasecampAPIError()

