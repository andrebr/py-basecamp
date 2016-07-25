import json
from .base import Basecamp
from .exceptions import BasecampAPIError


class TodoList(Basecamp):
    """
    Operations on Todo Lists in the API
    """
    endpoint = 'todolists'

    def fetch(self, project_id=None, todo_list_filter=None):
        """
        Get a todo list, or a list of todo lists.

        :param todo_list_filter: Optional, 'completed' or 'trashed'.
        :rtype dictionary: dictionary of todo_list_id see `the following <https://\
        github.com/37signals/bcx-api/blob/master/sections/\
        todo_lists.md#get-all-lists-across-projects>`_ for the returned structure.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.TodoList(account_url, access_token)
        >>> todo_lists = api.fetch()
        """

        if project_id:
            self.endpoint = "{0}/{1}/{2}".format('projects', project_id, self.endpoint)
        else:
            self.endpoint = "{0}".format(self.endpoint)

        if todo_list_filter:
            self.endpoint += '/{0}.json' % todo_list_filter
        else:
            self.endpoint += '.json'

        request = self.get(self.construct_url())

        if request.status_code == 200:
            return json.loads(request.content)

        raise BasecampAPIError(json.loads(request.content).get('error'))

    def create(self, name, description='', milestone_id=None, private=False, tracked=False):
        """
        Create a new todo list in a basecamp account.

        :param name: New todo list name.
        :param description: New todo list description.
        :param milestone_id: Id of milestone_id.
        :param private: Boolean if private todo list.
        :param tracked: Boolean if tracked todo list.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.TodoList(account_url, access_token)
        >>> todo_list = api.create('My New List', 'New stuff to do')
        """

        data = dict(
            name=name,
            description=description,
            milestone_id=milestone_id,
            private=private,
            tracked=tracked
        )

        request = self.post(self.construct_url(), payload=json.dumps(data))

        if request.status_code == 201:
            return json.loads(request.content)
        elif request.status_code == 403:
            # not allowed to create todo lists
            # or reached the todo list limit
            raise BasecampAPIError()

        raise BasecampAPIError(request.content)

    def update(self, todo_list_id, name, description='', milestone_id=None, private=False, tracked=False):
        """
        Update an existing basecamp todo list.

        :param name: New todo list name.
        :param description: New todo list description.
        :param milestone_id: Id of milestone_id.
        :param private: Boolean if private todo list.
        :param tracked: Boolean if tracked todo list.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.todo list(account_url, access_token)
        >>> todo lists = api.update(675, 'Giant Steps', 'John Coltrane')

        """
        self.endpoint = 'todo_lists/{0}.json'.format(todo_list_id)

        data = dict(
            name=name,
            description=description,
            milestone_id=milestone_id,
            private=private,
            tracked=tracked
        )

        request = self.put(self.construct_url(), payload=json.dumps(data))

        if request.status_code == 200:
            return json.loads(request.content)
        elif request.status_code == 403:
            # not allowed to create todo lists
            # or reached the todo list limit
            raise BasecampAPIError()

        raise BasecampAPIError(request.content)

    def remove(self, todo_list_id):
        """
        Remove a todo list

        :param todo_list_id: id of the todo list to delete.
        :rtype: True if the todo list is removed, otherwise \
        a :class:`BasecampAPIError` exception.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.todo list(account_url, access_token)
        >>> removed = api.remove(675)
        """
        self.endpoint = 'todo_lists/{0}.json'.format(todo_list_id)
        request = self.delete(self.construct_url())

        if request.status_code == 204:
            return True
        elif request.status_code == 403:
            raise BasecampAPIError()

        raise BasecampAPIError()


    def todo_items(self, todo_list_id):
        """
        Get a list of todo list items.

        :param todo_list_id: todo list id
        :rtype dictionary: dictionary of todo_items see `the following <https://\
        github.com/37signals/bcx-api/blob/master/sections/\
        todo_itemss.md#get-all-lists-across-projects>`_ for the returned structure.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.TodoList(account_url, access_token)
        >>> todo_itemss = api.fetch()
        """

        self.endpoint = '{0}/{1}/todo_items.json'.format(self.endpoint, todo_list_id)

        request = self.get(self.construct_url())

        if request.status_code == 200:
            return json.loads(request.content)

        raise BasecampAPIError(json.loads(request.content).get('error'))
