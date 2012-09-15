"""
Project class

https://github.com/37signals/bcx-api/blob/master/sections/projects.md
"""
import json
from .base import Basecamp
from .exceptions import BasecampAPIError


class Project(Basecamp):
    """
    Operations on Projects in the API
    """
    endpoint = 'projects'

    def fetch(self, project=None, archived=False):
        """
        Get a project, or a list of projects.
        """
        if archived:
            self.endpoint = 'projects/archived.json'

        if project:
            self.endpoint = '{0}/{1}.json'.format(self.endpoint, project)
        else:
            self.endpoint = "{0}.json".format(self.endpoint)

        request = self.get(self.construct_url())

        if request.status_code == 200:
            return json.loads(request.content)

        raise BasecampAPIError(json.loads(request.content).get('error'))

    def create(self, name, description):
        """
        Create a project.
        """
        self.endpoint = 'projects'

        data = dict(
            name=name,
            description=description
        )

        request = self.post(self.construct_url(),
            post_data=json.dumps(data))

        if request.status_code == 201:
            return json.loads(request.content)
        elif request.status_code == 403:
            # not allowed to create projects
            # or reached the project limit
            raise BasecampAPIError()

        raise BasecampAPIError(request.content)


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
