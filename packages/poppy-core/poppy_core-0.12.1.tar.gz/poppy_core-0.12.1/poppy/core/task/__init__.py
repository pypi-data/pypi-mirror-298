# -*- coding: utf-8 -*-
from .task import Task

__all__ = ["Task", "TaskError"]


class TaskError(Exception):
    """
    Error associated to tasks.
    """
