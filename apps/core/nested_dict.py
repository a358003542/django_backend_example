#!/usr/bin/env python
# -*-coding:utf-8-*-


from collections import defaultdict
import sys


def flatten_nested_items(dictionary):
    """
    Flatten a nested_dict.
    iterate through nested dictionary (with iterkeys() method)
         and return with nested keys flattened into a tuple
    """
    if sys.hexversion < 0x03000000:
        keys = dictionary.iterkeys
        keystr = "iterkeys"
    else:
        keys = dictionary.keys
        keystr = "keys"
    for key in keys():
        value = dictionary[key]
        if hasattr(value, keystr):
            for keykey, value in flatten_nested_items(value):
                yield (key,) + keykey, value
        else:
            yield (key,), value


class _recursive_dict(defaultdict):
    """
    Parent class of nested_dict.
    Defined separately for _nested_levels to work
    transparently, so dictionaries with a specified (and constant) degree of nestedness
    can be created easily.
    The "_flat" functions are defined here rather than in nested_dict because they work
        recursively.
    """

    def iteritems_flat(self):
        """Iterate through items with nested keys flattened into a tuple."""
        for key, value in flatten_nested_items(self):
            yield key, value

    def iterkeys_flat(self):
        """Iterate through keys with nested keys flattened into a tuple."""
        for key, value in flatten_nested_items(self):
            yield key

    def itervalues_flat(self):
        """Iterate through values with nested keys flattened into a tuple."""
        for key, value in flatten_nested_items(self):
            yield value

    items_flat = iteritems_flat
    keys_flat = iterkeys_flat
    values_flat = itervalues_flat

    def to_dict(self, input_dict=None):
        """Convert the nested dictionary to a nested series of standard ``dict`` objects."""
        #
        # Calls itself recursively to unwind the dictionary.
        # Use to_dict() to start at the top level of nesting
        plain_dict = dict()
        if input_dict is None:
            input_dict = self
        for key in input_dict.keys():
            value = input_dict[key]
            if isinstance(value, _recursive_dict):
                # print "recurse", value
                plain_dict[key] = self.to_dict(value)
            else:
                # print "plain", value
                plain_dict[key] = value
        return plain_dict

    def __str__(self, indent=None):
        """Representation of self as a string."""
        import json
        return json.dumps(self.to_dict(), indent=indent)


def _recursive_update(nd, other):
    for key, value in other.items():
        # print ("key=", key)
        if isinstance(value, (dict,)):

            # recursive update if my item is nested_dict
            if isinstance(nd[key], (_recursive_dict,)):
                # print ("recursive update", key, type(nd[key]))
                _recursive_update(nd[key], other[key])

            # update if my item is dict
            elif isinstance(nd[key], (dict,)):
                # print ("update", key, type(nd[key]))
                nd[key].update(other[key])

            # overwrite
            else:
                # print ("self not nested dict or dict: overwrite", key)
                nd[key] = value
        # other not dict: overwrite
        else:
            # print ("other not dict: overwrite", key)
            nd[key] = value
    return nd


class _any_type(object):
    pass


def _nested_levels(level, nested_type):
    """Helper function to create a specified degree of nested dictionaries."""
    if level > 2:
        return lambda: _recursive_dict(_nested_levels(level - 1, nested_type))
    if level == 2:
        if isinstance(nested_type, _any_type):
            return lambda: _recursive_dict()
        else:
            return lambda: _recursive_dict(
                _nested_levels(level - 1, nested_type))
    return nested_type


class nested_dict(_recursive_dict):
    """
    Nested dict.
    Uses defaultdict to automatically add levels of nested dicts and other types.
    """

    def update(self, other):
        """Update recursively."""
        _recursive_update(self, other)

    def __init__(self, *param, **named_param):
        """
        Constructor.
        Takes one or two parameters
            1) int, [TYPE]
            1) dict
        """
        if not len(param):
            self.factory = nested_dict
            defaultdict.__init__(self, self.factory)
            return

        if len(param) == 1:
            # int = level
            if isinstance(param[0], int):
                self.factory = _nested_levels(param[0], _any_type())
                defaultdict.__init__(self, self.factory)
                return
            # existing dict
            if isinstance(param[0], dict):
                self.factory = nested_dict
                defaultdict.__init__(self, self.factory)
                nested_dict_from_dict(param[0], self)
                return

        if len(param) == 2:
            if isinstance(param[0], int):
                self.factory = _nested_levels(*param)
                defaultdict.__init__(self, self.factory)
                return

        raise Exception("nested_dict should be initialised with either "
                        "1) the number of nested levels and an optional type, or "
                        "2) an existing dict to be converted into a nested dict "
                        "(factory = %s. len(param) = %d, param = %s"
                        % (self.factory, len(param), param))


def nested_dict_from_dict(orig_dict, nd):
    """Helper to build nested_dict from a dict."""
    for key, value in orig_dict.items():
        if isinstance(value, (dict,)):
            nd[key] = nested_dict_from_dict(value, nested_dict())
        else:
            nd[key] = value
    return nd
