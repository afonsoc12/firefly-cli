from datetime import datetime

import tabulate as tab


def prompt_continue(extra_line=True, extra_msg=""):
    extra_line = "\n" if extra_line else ""
    valid_ans = ("y", "yes")
    ans = input(f"{extra_line}Would you like to proceed{extra_msg}? (y/n): ")

    return ans.lower() in valid_ans


def json_serial(obj, iso_format=True):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        if iso_format:
            return obj.isoformat()
        else:
            return obj.strftime("%a, %Y-%m-%d %H:%M:%S")
    raise TypeError("Type %s not serializable" % type(obj))


def date_to_datetime(s):
    """Converts a string representation of a date to a datetime object."""
    return datetime.strptime(s, "%Y-%m-%d").astimezone()


def datetime_to_datetime(s):
    """Converts a string representation of a datetime to a datetime object."""
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").astimezone()


def tabulate(data, headers="keys", tablefmt="psql", header_fmt=None):
    if header_fmt == "capitalise_from_snake":
        headers = [snake_to_spaced(k, capitalise=True) for k in data]
    return tab.tabulate(data, headers=headers, tablefmt=tablefmt)


def snake_to_spaced(s, capitalise=False):
    words = s.split("_")

    if capitalise:
        words = [w.capitalize() for w in words]

    return " ".join(words).strip()
