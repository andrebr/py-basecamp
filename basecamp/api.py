# -*- coding: utf-8 -*-
"""
basecamp
------------

This module exists in order to do * imports from.

If this was handled in __init__, there would be issues with
getting the version and handling dependencies in setup.py.
"""

from .auth import Auth
from .projects import Project
from .people import Person
from .documents import Document
from .base import Basecamp
from .todo_lists import TodoList
from .todos import Todo
from .comments import Comment