from typing import Any

from . import DPType, Responses


class Boolean(DPType):
    """
    A `Boolean` corresponds to the JSON-type 'boolean'.
    """
    TYPE = bool

    def make(self, json, loc: str) -> tuple[Any, str, int]:
        return (
            self.TYPE(json),
            Responses().GOOD.msg,
            Responses().GOOD.status
        )
