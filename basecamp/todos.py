import json
from .base import Basecamp
from .exceptions import BasecampAPIError


class Todo(Basecamp):
    """
    Operations on Todo Lists in the API
    """
    endpoint = 'projects'

    def fetch(self, project_id, todo_list_id=None, todo_id=None, todo_filter=None, due_since_date=None):
        """
        Get a todo list item, or a list of todo list items.

        :param todo_filter: 'complated', 'remaining', 'trashed'
        :param due_since_date: A date for filtering all todos due after date.
        :param todo_items: todo list id or None
        :rtype dictionary: dictionary of todo_items see `the following <https://\
        github.com/37signals/bcx-api/blob/master/sections/\
        todo_itemss.md#get-all-lists-across-projects>`_ for the returned structure.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.TodoList(account_url, access_token)
        >>> todo_itemss = api.fetch()

        Per Project:

        GET /projects/1/todos.json shows a list of all to-dos for this project; completed and remaining.
        GET /projects/1/todos/completed.json shows a list of all completed to-dos for this project.
        GET /projects/1/todos/remaining.json shows a list of all remaining/active to-dos for this project.
        GET /projects/1/todos.json?due_since=2014-07-10 will return all the to-dos due after the date specified.

        Get To do

        GET /projects/1/todos/1.json will return the specified to-do.

        Per To-do List:

        GET /projects/1/todolists/1/todos.json shows a list of all to-dos for this to-do list; completed and remaining.
        GET /projects/1/todolists/1/todos/completed.json shows a list of all completed to-dos for this to-do list.
        GET /projects/1/todolists/1/todos/remaining.json shows a list of all remaining to-dos for this to-do list.
        GET /projects/1/todolists/1/todos/trashed.json shows a list of all trashed to-dos for this to-do list.


        """

        self.endpoint += "/{0}/".format(project_id)

        if todo_list_id:
            self.endpoint += 'todolists/{0}/todos'.format(todo_list_id)

        if todo_id:
            self.endpoint += 'todos/{0}'.format(todo_id)

        if todo_filter:
            self.endpoint += '/{0}'.format(todo_filter)

        self.endpoint += '.json'

        if due_since_date:
            self.endpoint += '?due_since={0}'.format(due_since_date)

        request = self.get(self.construct_url())

        if request.status_code == 200:
            return json.loads(request.content)

        try:
            raise BasecampAPIError(json.loads(request.content).get('error'))
        except:
            pass

    def complete(self, todo_item_id):
        """
        Complete a todo list item

        :param todo_item_id: id of the todo item to copmlete.
        :rtype: True if the todo list is removed, otherwise \
        a :class:`BasecampAPIError` exception.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.todo list(account_url, access_token)
        >>> removed = api.remove(675)
        """
        self.endpoint = '{0}/{1}/complete.json'.format(self.endpoint, todo_item_id)
        request = self.put(self.construct_url())

        if request.status_code == 200:
            return True
        elif request.status_code == 403:
            raise BasecampAPIError()

        raise BasecampAPIError()

    def uncomplete(self, todo_item_id):
        """
        UnComplete a todo list item

        :param todo_item_id: id of the todo item to copmlete.
        :rtype: True if the todo list is removed, otherwise \
        a :class:`BasecampAPIError` exception.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.todo list(account_url, access_token)
        >>> removed = api.remove(675)
        """
        self.endpoint = '{0}/{1}/uncomplete.json'.format(todo_item_id)
        request = self.put(self.construct_url())

        if request.status_code == 200:
            return True
        elif request.status_code == 403:
            raise BasecampAPIError()

        raise BasecampAPIError()

    def create(self, project_id, todo_list_id, content):
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
        >>> todo_items = api.create('My New List', 'New stuff to do')
        """
        self.endpoint = '{0}/{1}/todolists/{2}/todos.json'.format(
            self.endpoint,
            project_id,
            todo_list_id)

        data = {
            'content': content
        }

        request = self.post(self.construct_url(), payload=json.dumps(data))

        if request.status_code == 201:
            return json.loads(request.content)
        elif request.status_code == 403:
            # not allowed to create todo lists
            # or reached the todo list limit
            raise BasecampAPIError()

        raise BasecampAPIError(request.content)

    def update(self, project_id, todo_id, content):
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
        self.endpoint = '{0}/{1}/todos/{2}.json'.format(
            self.endpoint,
            project_id,
            todo_id)

        data = {
            'content': content
        }

        request = self.put(self.construct_url(), payload=json.dumps(data))

        if request.status_code == 200:
            return json.loads(request.content)
        elif request.status_code == 403:
            # not allowed to create todo lists
            # or reached the todo list limit
            raise BasecampAPIError()

        raise BasecampAPIError(request.content)

    def remove(self, project_id, todo_id):
        """
        Remove a todo list

        :param todo_items_id: id of the todo list to delete.
        :rtype: True if the todo list is removed, otherwise \
        a :class:`BasecampAPIError` exception.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.todo list(account_url, access_token)
        >>> removed = api.remove(675)
        """
        self.endpoint = '{0}/{1}/todos/{2}.json'.format(
            self.endpoint,
            project_id,
            todo_id)

        request = self.delete(self.construct_url())

        if request.status_code == 204:
            return True
        elif request.status_code == 403:
            raise BasecampAPIError()

        raise BasecampAPIError()
