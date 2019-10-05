#!/usr/local/bin/python3
import json

class Serializable(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # hack to fix _json.so make_encoder serialize properly
        self.__setitem__('dummy', 1)

    def _myattrs(self):
        return [
            (x, self._repr(getattr(self, x)))
            for x in self.__dir__()
            if x not in Serializable().__dir__()
        ]

    def _repr(self, value):
        if isinstance(value, (str, int, float, list, tuple, dict)):
            return value
        else:
            return repr(value)

    def __repr__(self):
        return '<%s.%s object at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self))
        )

    def keys(self):
        return iter([x[0] for x in self._myattrs()])

    def values(self):
        return iter([x[1] for x in self._myattrs()])

    def items(self):
        return iter(self._myattrs())