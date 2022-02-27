from datetime import datetime


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
