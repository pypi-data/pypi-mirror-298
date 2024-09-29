from typing import Any
import abc

from data_plumber_http.settings import Responses


class DPType(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def TYPE(self):
        raise NotImplementedError(
            "Property 'TYPE' needs to be defined when using abstract base 'DPType'."
        )

    @abc.abstractmethod
    def make(self, json, loc: str) -> tuple[Any, str, int]:
        raise NotImplementedError(
            "Method 'make' needs to be defined when using abstract base 'DPType'."
        )

    @property
    def __name__(self):
        return self.TYPE.__name__

    def __or__(self, other):
        class _(DPType):
            _TYPES = [self, other]
            TYPE = self.TYPE | other.TYPE
            __name__ = f"{self.__name__} | {other.__name__}"
            def make(self, json, loc: str) -> tuple[Any, str, int]:
                # iterate all possible make-methods in _TYPES
                last = None
                for _type in self._TYPES:
                    # check whether types match at all
                    if not isinstance(json, _type.TYPE):
                        continue
                    # try to make instance of DPType
                    last = _type.make(json, loc)
                    # try next option if not successful
                    if last[2] != Responses().GOOD.status:
                        continue
                    # return if everything went well
                    return (
                        last[0],
                        Responses().GOOD.msg,
                        Responses().GOOD.status
                    )
                # return info from latest attempt of making an instance
                if last is not None:
                    return (None, last[1], last[2])
                # never made a type-match > raise error
                raise ValueError(
                    "Union type constructor called with bad type. "
                    + f"'{type(json).__name__}' not in '{self.__name__}'."
                )
        return _()


from .array import Array
from .boolean import Boolean
from .float import Float
from .integer import Integer
from .null import Null
from .object import Object
from .string import String
from .uri import Uri
from .url import Url
from .file_system_object import FileSystemObject
# import last due to dependence on base-types
from .number import Number
from .any import Any


__all__ = [
    "DPType",
    "Any", "Array", "Boolean", "Float", "Integer", "Null", "Number", "Object",
    "String", "Uri", "Url", "FileSystemObject",
]
