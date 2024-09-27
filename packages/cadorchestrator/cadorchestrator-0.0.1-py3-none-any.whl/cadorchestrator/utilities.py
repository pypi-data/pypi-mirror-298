"""
A module containting utilitiy functions
"""

import pathlib


def clean_dict(data: dict) -> dict:
    """
    Clean the input dictionary (recursively). Removing any keys where the value is
    none, changing pathlib.Path to strings and converting tuples to strings.

    The input is a single dictionary, the output is a cleaned dictionary.
    """
    # iterate over entries
    keys_to_delete = []
    for key, value in data.items():
        # remove empty entries
        if value is None:
            keys_to_delete.append(key)
        else:
            data[key] = _clean_object(value)
    # delete empty entries
    for key in keys_to_delete:
        del data[key]
    return data


def _clean_object(obj: object) -> object:
    # clean up lists
    if isinstance(obj, list):
        return [_clean_object(x) for x in obj]
    # clean up dicts
    if isinstance(obj, dict):
        return clean_dict(obj)
    if isinstance(obj, tuple):
        # convert to string like "(1,2,3)"
        return str(obj)
    if isinstance(obj, pathlib.Path):
        # convert to string
        return str(obj)
    return obj


def get_nested_dict(dictionary, keylist, add_if_missing=False):
    """
    Return the object nested within a dictionary, given the list of
    key names. Optionally an empty dictionary can be added if the
    key is missing.
    """
    d = dictionary
    for key_name in keylist:
        if key_name not in d:
            if add_if_missing:
                d[key_name] = {}
            else:
                raise KeyError(f"Couldn't access {keylist} in dict {dictionary}. No key {key_name}")
        if not isinstance(d[key_name], dict):
            raise TypeError(f"Couldn't access {keylist} in dict {dictionary}. "
                            f"{key_name} has a non-dict value")
        d = d[key_name]
    return d
