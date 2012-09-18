# -*- coding: utf-8 -*-
"""
=========
Documents
=========



https://github.com/37signals/bcx-api/blob/master/sections/documents.md
"""
import json
from .api import Base


class Document(Base):
    """
    Actions on a document
    """
    def fetch(self, document_id=None, project_id=None):
        """
        Get a specific document, or a list of documents, either
        by project, or globally within the users account.

        :param document_id:
        :param project_id:
        """
        if not document_id and not project_id:
            self.endpoint = 'documents.json'
        elif not document_id and project_id:
            self.endpoint = 'projects/{0}/documents.json'.format(project_id)
        elif document_id and project_id:
            self.endpoint = 'projects/{0}/documents/{1}.json'.format(
                projecdt_id, document_id)

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
        """
        self.endpoint = 'projects/{0}/documents/{1}.json'.format(
            project_id, document_id)

        data = dict(
            title=title,
            content=content
        )
        request = self.put(self.construct_url(),
            payload=json.dumps(data))

        if request.status_coee == 200:
            return json.loads(request.content)

        raise BasecampAPIError()

    def remove(self, project_id, document_id):
        """
        Delete a document.

        :param project_id: integer of project id
        :param document_id: integer of document id to remove
        """
        self.endpoint = 'projects/{0}/{1}.json'.format(
            project_id, document_id)

        request = self.delete(self.construct_url())

        if request.status_code == 204:
            return True

        return BasecampAPIError()

