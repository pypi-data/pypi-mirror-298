import math
from collections.abc import Iterable


def is_sequence(obj):
    if isinstance(obj, str):
        return False
    try:
        tuple(obj)
        return True
    except:
        return False


def __get_as_collection(obj, collection_f, error_message):
    if is_sequence(obj):
        return collection_f(obj)
    else:
        raise ValueError(error_message)


def get_as_tuple(obj, error_message):
    return __get_as_collection(obj, tuple, error_message)


def get_as_list(obj, error_message):
    return __get_as_collection(obj, list, error_message)


def is_collection(obj):
    """Returns True if an object can be iterated but is not a string or bytes"""
    return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))


def is_float_like(value):
    try:
        float(value)
        return True
    except:
        return False


def get_as_float(value):
    if not is_float_like(value):
        raise ValueError("'%s' is not a number" % (value,))
    else:
        return float(value)


def get_as_float_or_nan(value):
    if value is None:
        return math.nan
    else:
        return get_as_float(value)


def __is_number(value):
    try:
        value + 1
        return True
    except:
        return False


def __assert_is_number(name, value):
    if not __is_number(value):
        raise TypeError(f"Argument '{name}' has to be a number")


def __is_int(value):
    try:
        return int(value) == value
    except:
        return False


def __assert_is_int(name, value):
    if not __is_int(value):
        raise TypeError(f"Argument '{name}' has to be an integer")


def __assert_is_bool(name, value):
    if not isinstance(value, bool):
        raise TypeError(f"Argument '{name}' has to be a boolean")


def is_string(value):
    return isinstance(value, str)

def __assert_is_string(name, value, allow_empty = True):
    if not is_string(value):
        raise TypeError(f"'{name}' has to be a string")
    if not allow_empty:
        if len(value.strip()) == 0:
            raise ValueError(f"'{name}' cannot be blank or empty")


def __is_list_of_specific_type(name, value, error_message_template, test_f):
    if not is_sequence(value):
        raise TypeError(f"'{name}' has to be a list")
    for i in value:
        if not test_f(i):
            raise TypeError(error_message_template % (name,))


def __assert_is_list_of_strings(name, value):
    __is_list_of_specific_type(name,
                               value,
                               "'%s' has to be a list of strings",
                               is_string)


def __assert_is_list_of_numbers(name, value):
    __is_list_of_specific_type(name,
                               value,
                               "'%s' has to be a list of numbers",
                               __is_number)


def __assert_is_list_of_integers(name, value):
    __is_list_of_specific_type(name,
                               value,
                               "'%s' has to be a list of integers",
                               __is_int)


def ensure_correct_args(*checks):
    """Throws an exception if an argument is of the wrong type.

    Checks are in the form:

    (name of the argument, expected type, actual value)

    expected type could be:

    string
    !string (for non empty/blank strings)
    num
    int
    bool
    [string]
    [num]
    [int]
    ?type (for parameters that can be null)
    """
    for arg_name, arg_type, arg_value in checks:
        if arg_type.startswith("?"):
            if arg_value is None:
                continue
            else:
                arg_type = arg_type[1:]
        if arg_type == "string":
            __assert_is_string(arg_name, arg_value)
        elif arg_type == "!string":
            __assert_is_string(arg_name, arg_value, False)
        elif arg_type == "int":
            __assert_is_int(arg_name, arg_value)
        elif arg_type == "num":
            __assert_is_number(arg_name, arg_value)
        elif arg_type == "bool":
            __assert_is_bool(arg_name, arg_value)
        elif arg_type == "[string]":
            __assert_is_list_of_strings(arg_name, arg_value)
        elif arg_type == "[num]":
            __assert_is_list_of_numbers(arg_name, arg_value)
        elif arg_type == "[int]":
            __assert_is_list_of_integers(arg_name, arg_value)
        else:
            raise ValueError(f"Invalid type '{arg_type}")
