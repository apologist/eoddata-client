import datetime

class Error(Exception):
    """Base error for this module."""


class FunctionRecursionDepthReachedError(Error):
    """Function reached the maximum recursion depth"""


class ObjectProxy(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__name__ = wrapped.__name__
        except AttributeError:
            pass

    @property
    def __class__(self):
        return self.wrapped.__class__

    def __getattr__(self, name):
        return getattr(self.wrapped, name)


class BoundFunctionWrapper(ObjectProxy):

    def __init__(self, wrapped):
        super(BoundFunctionWrapper, self).__init__(wrapped)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


class RecursionDepthManager(object):

    def __init__(self, func, max_depth=3):
        self.func = func
        self.max_recursion_depth = max_depth
        self.func.recursion_depth = 0

    def __call__(self, *args, **kwargs):
        if self.func.recursion_depth > self.max_recursion_depth:
            raise FunctionRecursionDepthReachedError
        self.func.recursion_depth += 1
        result = self.func(*args, **kwargs)
        self.func.recursion_depth = 0
        return result

recursion_depth_managed = RecursionDepthManager


def string_to_datetime(iso8601_datetime_string):
    """
    Converts ISO 8601 datetime string to Python datetime

    Args:
        iso8601_datetime_string (str): ISO 8601 datetime string

    Returns:
        datetime.datetime object

    Raises:
        ValueError

    """
    try:
        return datetime.datetime.strptime(iso8601_datetime_string, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return datetime.datetime.strptime(iso8601_datetime_string, '%Y-%m-%dT%H:%M:%S.%f')
