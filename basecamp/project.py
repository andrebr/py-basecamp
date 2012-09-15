# -*- coding: utf-8 -*-
"""
Project class

https://github.com/37signals/bcx-api/blob/master/sections/projects.md
"""
from .api import Base


class Project(Base):
    """
    Operations on Projects in the API
    """
    def fetch(self, project=None):
        """
        Get a project, or a list of projects.
        """

    def create(self, name, description):
        """
        Create a project.
        """

    def update(self, project_id, name, description):
        """
        Update a project
        """

    def archive(self, project_id, archive=True):
        """
        Archive or unarchive a project
        """

    def delete(self, project):
        """
        Delete a project
        """
