# -*- coding: utf-8 -*-

"""
#@Filename : base_collections
#@Date : [7/29/2018 12:49 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import json
import sys, os
from collections import OrderedDict
from collections.__init__ import OrderedDict
from collections.abc import MutableMapping, MutableSequence
from collections.abc import KeysView, MappingView, Set, ItemsView, ValuesView
from pathlib import Path
from copy import deepcopy
from typing import Any, MutableSequence, MutableMapping


import toml
import yaml

################################################################################
## Third-Party Imports
from dataclasses import dataclass
from melddict import MeldDict

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.gc3logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

DEFAULT_INDENT = 4
DEFAULT_FLOW_STYLE = False

class ListBase(MutableSequence):
    """A container for manipulating lists of hosts"""

    def __init__(self, data=None):
        super().__init__()
        self._name = {__class__.__name__}
        if (data is not None):
            self._list = list(data)
        else:
            self._list = list()

    def __repr__(self):
        return "<{0} {1}>".format(self._name, self._list)

    def __len__(self):
        """List length"""
        return len(self._list)

    def __getitem__(self, index):
        """Get a list item"""
        return self._list[index]

    def __delitem__(self, index):
        """Delete an item"""
        del self._list[index]

    def __setitem__(self, index, val):
        # optional: self._acl_check(val)
        self._list[index] = val
        return None

    def __str__(self):
        return str(self._list)

    def insert(self, index, val):
        # optional: self._acl_check(val)
        self._list.insert(index, val)

    def append(self, val):
        self.insert(len(self._list), val)

    def __eq__(self, other):
        return self._list == other



class KeysViewBase(KeysView):
    def __init__(self, mapping, filters: Optional[List[Callable[[str], bool]]] = None):
        self._mapping = mapping
        self._filters = filters if filters else []

    def __contains__(self, key: str) -> bool:
        if not key in self._mapping:
            return False
        if self._filters:
            filter_results = [filter(key) for filter in self._filters]
            return all(filter_results)
        return True

    def __len__(self):
        keys = [k for k in self._mapping if k in self]
        return len(keys)

    def __iter__(self):
        yield from (k for k in self._mapping if k in self)

    def __repr__(self):
        _keys = [k for k in self]
        return f'{self.__class__.__name__}(mapping={self._mapping.__class__.__name__}, filters={len(self._filters)}, keys={_keys})'

    def __str__(self):
        return repr(self)

class ValuesViewBase(ValuesView):

    def __init__(self, mapping, filters: Optional[List[Callable[[str], bool]]] = None):
        self._mapping = mapping
        self._filters = filters if filters else []

    def __contains__(self, value):
        for key in self._mapping:
            v = self._mapping[key]
            if v is value or v == value:
                if self._filters:
                    filter_results = [filter(value) for filter in self._filters]
                    return all(filter_results)
                return True
        return False

    def __iter__(self):
        yield from (self._mapping[k] for k in self._mapping if self._mapping[k] in self)

    def __len__(self):
        values = [v for v in self._mapping.values() if v in self]
        return len(values)

    def __repr__(self):
        _values = [v for v in self._mapping.values() if v in self]
        return f'{self.__class__.__name__}(mapping={self._mapping.__class__.__name__}, filters={len(self._filters)}, values={_values})'

    def __str__(self):
        return repr(self)

class ItemsViewBase(ItemsView):

    def __init__(self, mapping, filters: Optional[List[Callable[[str, Any], bool]]] = None):
        self._mapping = mapping
        self._filters = filters if filters else []

    @classmethod
    def _from_iterable(self, it):
        return set(it)

    def __contains__(self, item):
        key, value = item
        try:
            v = self._mapping[key]
        except KeyError:
            return False
        else:
            is_contained = v is value or v == value
            if is_contained:
                if self._filters:
                    filter_results = [filter(key, v) for filter in self._filters]
                    return all(filter_results)
                return is_contained

    def __len__(self):
        items = [(k,v) for k,v in self._mapping.items() if (k,v) in self]
        return len(items)

    def __iter__(self):
        yield from ((k, self._mapping[k]) for k in self._mapping if (k, self._mapping[k]) in self)

    def __repr__(self):
        _items = [f'{k}={v}' for k,v in self._mapping.items() if (k,v) in self]
        _items = ', '.join(_items)
        return f'{self.__class__.__name__}(mapping={self._mapping.__class__.__name__}, filters={len(self._filters)}, items=[{_items}])'

    def __str__(self):
        return repr(self)



class DictBase(MutableMapping):
    """
    Mapping that works like both a dict and a mutable object, i.e. d = D(foo='bar')
    and
    d.foo returns 'bar'

    """

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        self.__dict__.update(*args, **kwargs)
        self._name = {__class__.__name__}

    # The next five methods are requirements of the ABC.
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    # The final two methods aren't required, but nice for demo purposes:
    def __str__(self):
        """returns simple dict representation of the mapping"""
        return str('{}: {}'.format(__class__, str(self)))

    def __repr__(self):
        """echoes class, id, & reproducible representation in the REPL"""
        return '{}, {}({})'.format(super().__repr__(), __class__, self)


class OrderedDictBase(MutableMapping):
    """
    Mapping that works like both a dict and a mutable object, i.e. d = D(foo='bar')
    and
    d.foo returns 'bar'

    """

    def __init__(self, *args, **kwargs):
        """
        Use the object dict

        :param args:
        :param kwargs:
        """
        self._d = OrderedDict(*args, **kwargs)
        self._name = {__class__.__name__}

    # The next five methods are requirements of the ABC.
    def __setitem__(self, key, value):
        self._d[key] = value
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self._d[key]

    def __delitem__(self, key):
        del self._d[key]
        _ = self.__dict__.pop(key)

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    # The final two methods aren't required, but nice for demo purposes:
    def __str__(self):
        """returns simple dict representation of the mapping"""
        k_v = ', '.join([f'{k}={v}' for k, v in self.items()])
        s = f'<{self.__class__.__name__} values={len(self)}: {k_v} >'
        return s

    def __repr__(self):
        """echoes class, id, & reproducible representation in the REPL"""
        k_v = ', '.join([f'{k}={v}' for k, v in self.items()])
        r = f'{self.__class__.__name__}({k_v})'
        return r

    # def keys(self):
    #     return super().keys()

    def keys(self, filters: Optional[List[Callable[[str], bool]]] = None) -> KeysViewBase:
        """D.keys() -> a set-like object providing a view on D's keys

        :param filters:  List of callables excluding the key if any of them returns False
        :return:
        """
        return KeysViewBase(self, filters=filters)

    def items(self, filters: Optional[List[Callable[[str, Any], bool]]]  = None) -> ItemsViewBase:
        "D.items() -> a set-like object providing a view on D's items"
        return ItemsViewBase(self, filters=filters)

    def values(self, filters: Optional[List[Callable[[str], bool]]] = None) -> ValuesViewBase:
        "D.values() -> an object providing a view on D's values"
        return ValuesViewBase(self, filters=filters)

    def lkeys(self):
        return list(self.keys())

    def lvalues(self):
        return list(self.values())

    # def items(self):
    #     return super().items()

    def litems(self):
        return list(self.items())

    def __eq__(self, other):
        return self._d == other


class OrderedDictAttrBase(OrderedDictBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        return self._d[key]


class CachedOrderedDictBase(OrderedDictBase):
    def __init__(self, path: Path):
        super().__init__()
        self._path = path
        if path.exists():
            with path.open('r') as fd:
                d = OrderedDictBase(yaml.load(fd))
            self._d = d

    def __setitem__(self, key, value):
        # make sure we're storing the fqdn
        super().__setitem__(key, value)
        self._update_cache()

    def __delitem__(self, key):
        super().__delitem__()
        self._update_cache()

    def __iter__(self):
        return iter(self._d)

    def _update_cache(self):
        with self._path.open('w') as fd:
            _debug(f'{self.__class__.__name__} caching value to file: {self._path}')
            yaml.dump(self._d, fd)


class NestedConfigListBase(ListBase):

    def __init__(self, data=None):
        super().__init__()
        if isinstance(data, MutableSequence):
            for v in data:
                if isinstance(v, MutableSequence):
                    self.append(NestedConfigListBase(v))
                if isinstance(v, MutableMapping):
                    self.append(NestedOrderedDictAttrListBase(v))
                else:
                    self.append(v)


class NestedOrderedDictAttrListBase(OrderedDictAttrBase):

    def __init__(self, mapping: Union[MutableMapping, None]=None):
        super().__init__()
        self._serializable = dict()

        if mapping:
            for key, value in mapping.items():
                if isinstance(value, MutableSequence):
                    self[key] = NestedConfigListBase(value)
                    self._serializable[key] = list(value)
                if isinstance(value, MutableMapping):
                    self[key] = NestedOrderedDictAttrListBase(value)
                    self._serializable[key] = dict(value)
                else:
                    self[key] = value
                    self._serializable[key] = value

    def __setitem__(self, key, value):
        # make sure we're storing the fqdn
        super().__setitem__(key, value)
        if isinstance(value, MutableSequence):
            self._serializable[key] = list(value)
        if isinstance(value, MutableMapping):
            self._serializable[key] = dict(value)
        else:
            self._serializable[key] = value

    def __delitem__(self, key):
        super().__delitem__(key)
        self._serializable.__delitem__(key)

    def __iter__(self):
        return iter(self._d)

    def __getattr__(self, key):
        return self._d[key]


    # The next five methods are requirements of the ABC.
    def __getitem__(self, key):
        return self.__dict__[key]


    def __str__(self) -> str:
        return str(self._serializable)

    # def __repr__(self):
    #     return f"<{self.__class__.__name__}: len(self) items>"

    def __repr__(self):
        return "{0}()".format(type(self))

    def export(self, file_path: Path, format: str = 'toml', overwrite: bool = False, export_formatting: DictStrAny=None)->Path:
        if not file_path.parent.exists():
            _warning(f"Parent directory, {file_path.parent}, does not exist, creating it")
            file_path.parent.mkdir()
        default_flow_style = export_formatting.get('default_flow_style', DEFAULT_FLOW_STYLE) if export_formatting else DEFAULT_FLOW_STYLE
        indent = export_formatting.get('indent', DEFAULT_INDENT) if export_formatting else DEFAULT_INDENT
        if file_path.exists() and not overwrite:
            raise RuntimeError(f"File already exists! file_path={file_path}, overwrite={overwrite}")
        with file_path.open('w') as fd:
            if format=='toml':
                toml.dump(self._serializable, fd)
            if format=='yaml':
                yaml.dump(self._serializable, fd, default_flow_style=default_flow_style, indent=indent)
            if format=='json':
                json.dump(self._serializable, fd, indent=indent)
        return file_path


    def as_dict(self) -> DictStrAny:
        return deepcopy(self._serializable)

    def as_dict_melded_with(self, other) -> DictStrAny:
        melded = MeldDict(self.as_dict())
        if hasattr(other, 'as_dict'):
            other = other.as_dict()
        melded.add(other)
        return melded

