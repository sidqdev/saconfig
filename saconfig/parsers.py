import typing
from .exceptions import *


TRUE_VALUES = {
    't',
    'y',
    'yes',
    'true',
    'on',
    '1',
}

FALSE_VALUES = {
    'f',
    'n',
    'no',
    'false',
    'off',
    '0',
}


def boolean_parser(value: str) -> bool:
    if isinstance(value, bool):
        return value
    if value.lower() in TRUE_VALUES:
        return True
    if value.lower() in FALSE_VALUES:
        return False
    raise ParseException(f"cant parse \"{value}\" to boolean")


def dict_parser(value: str, value_type: typing.Callable=str) -> dict:
    if isinstance(value, dict):
        return value
    data = dict()
    for r in value.split(','):
        k, v = r.split(":")
        data[k] = value_type(v)
    return data


special_parsers = {
    bool: boolean_parser,
    list: lambda x, value_type: x if isinstance(x, list) else list(map(value_type, x.split(','))),
    tuple: lambda x, value_type: x if isinstance(x, tuple) else tuple(map(value_type, x.split(','))),
    set: lambda x, value_type: x if isinstance(x, set) else set(map(value_type, x.split(','))),
    dict: dict_parser
}

