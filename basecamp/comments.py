import json
from .base import Basecamp
from .exceptions import BasecampAPIError


class Comment(Basecamp):
    """
    Operations on Comment Lists in the API
    """
    endpoint = 'projects'

    def create(self, project_id, topic, topic_id, content, subscribers=[]):
        """
        Create a new Comment list in a basecamp account.

        :param name: New Comment list name.
        :param description: New Comment list description.
        :param milestone_id: Id of milestone_id.
        :param private: Boolean if private Comment list.
        :param tracked: Boolean if tracked Comment list.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.CommentList(account_url, access_token)
        >>> Comment_items = api.create('My New List', 'New stuff to do')
        """
        self.endpoint = '{0}/{1}/{2}/{3}/comments.json'.format(
            self.endpoint,
            project_id,
            topic,
            topic_id)

        data = {
            'content': content,
            'subcribers': subscribers
        }

        request = self.post(self.construct_url(), payload=json.dumps(data))

        if request.status_code == 201:
            return json.loads(request.content)
        elif request.status_code == 403:
            # not allowed to create Comment lists
            # or reached the Comment list limit
            raise BasecampAPIError()

        raise BasecampAPIError(request.content)

    def remove(self, project_id, comment_id):
        """
        Remove a Comment list

        :param Comment_items_id: id of the Comment list to delete.
        :rtype: True if the Comment list is removed, otherwise \
        a :class:`BasecampAPIError` exception.

        >>> import basecamp.api
        >>> account_url = 'https://basecamp.com/12345/api/v1'
        >>> access_token = 'access_token'
        >>> api = basecamp.api.Comment list(account_url, access_token)
        >>> removed = api.remove(675)
        """
        self.endpoint = '{0}/{1}/comments/{2}.json'.format(
            self.endpoint,
            project_id,
            comment_id)
        request = self.delete(self.construct_url())

        if request.status_code == 204:
            return True
        elif request.status_code == 403:
            raise BasecampAPIError()

        raise BasecampAPIError()
