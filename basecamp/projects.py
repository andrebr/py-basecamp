"""
========
Projects
========

Create, edit, list, delete and archive projects in a Basecamp account.

See `the Basecamp API docs
<https://github.com/37signals/bcx-api/blob/master/sections/projects.md>`_
for more info.

An ``access_token`` is needed to perform any tasks within this class.
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

        :param project: project id or None
        :param archived: True or False - By default, non-archived projects\
        are not included in the list of projects returned.
        :rtype dictionary: dictionary of projects see `the following <https://\
        github.com/37signals/bcx-api/blob/master/sections/\
        projects.md#get-projects>`_ for the returned structure.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.Project(account_url, access_token)
        >>> projects = projects.fetch()
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
        Create a new project in a basecamp account.

        :param name: New project name.
        :param description: New project description.
        :rtype dictionary: Project details dictionary.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.Project(account_url, access_token)
        >>> projects = projects.create('My Favorites Things', 'John Coltrane')
        """

        data = dict(
            name=name,
            description=description
        )

        request = self.post(self.construct_url(), payload=json.dumps(data))

        if request.status_code == 201:
            return json.loads(request.content)
        elif request.status_code == 403:
            # not allowed to create projects
            # or reached the project limit
            raise BasecampAPIError()

        raise BasecampAPIError(request.content)

    def update(self, project_id, name, description):
        """
        Update an existing basecamp project.

        :param project_id: integer of project id to update.
        :param name: project name
        :param description: project description.
        :rtype dictionary: Dictionary of project details.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.Project(account_url, access_token)
        >>> projects = projects.update(675, 'Giant Steps', 'John Coltrane')

        """
        self.endpoint = 'projects/{0}'.format(project_id)

        data = dict(
            name=name,
            description=description
        )

        request = self.put(self.construct_url(), payload=json.dumps(data))

        if request.status_code == 200:
            return json.loads(request.content)
        elif request.status_code == 403:
            # not allowed to create projects
            # or reached the project limit
            raise BasecampAPIError()

        raise BasecampAPIError(request.content)

    def archive(self, project_id, archive=True):
        """
        Archive or unarchive a project.

        :param project_id: project id to archive or unarchive
        :param archive: boolean True to archive, False to unarchive
        :rtype dictionary: Dictionary of project details.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.Project(account_url, access_token)
        >>> projects = projects.archive(675, archive=True)
        """
        self.endpoint = 'projects/{0}'.format(project_id)
        data = dict(archived=archive)
        request = self.put(self.construct_url(), payload=json.dumps(data))

        if request.status_code == 200:
            json_data = json.loads(request.content)

            if archive and not json_data.get('archived'):
                # it should have been archived.
                raise BasecampAPIError('The project was not archived.')
            return json_data
        elif request.status_code == 403:
            raise BasecampAPIError()

        raise BasecampAPIError()

    def remove(self, project_id):
        """
        Remove a project

        :param project_id: id of the project to delete.
        :rtype: True if the project is removed, otherwise \
        a :class:`BasecampAPIError` exception.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.Project(account_url, access_token)
        >>> projects = projects.remove(675)
        """
        self.endpoint = 'projects/{0}.json'.format(project_id)
        request = self.delete(self.construct_url())

        if request.status_code == 204:
            return True
        elif request.status_code == 403:
            raise BasecampAPIError()

        raise BasecampAPIError()

    # Move to todo_list.
    def reorder_todo_lists(self, project_id, todo_list_ids):
        """
        Remove a todo list

        :param project_id: ID of project
        :param todo_list_ids: ids of the todo list to in order.
        :rtype: True if successfully reordered.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.todo list(account_url, access_token)
        >>> reordered = api.reorder([675, 674, 673])
        """
        self.endpoint = 'projects/{0}/todo_lists/reorder'.format(project_id)
        data = [
            {
                'todo-list': {
                    'id': x
                }
            } for x in todo_list_ids
        ]

        request = self.put(self.construct_url(), paylouad=json.dumps(data))

        if request.status_code == 204:
            return True
        elif request.status_code == 403:
            raise BasecampAPIError()

        raise BasecampAPIError()
