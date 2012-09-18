# -*- coding: utf-8 -*-
"""
=========
Documents
=========



https://github.com/37signals/bcx-api/blob/master/sections/documents.md
"""
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

    def create(self, title, content):
        """
        Create a new document.
        """

    def update(self, document_id, title, content):
        """
        Update a document.
        """

    def remove(self, document_id):
        """
        Delete a document.
        """
