import datetime


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
