from __future__ import annotations as _annotations

from itertools import count as _count
from typing import (
    Any as _Any,
    Generator as _Generator,
    Callable as _Callable,  # noqa: F401
    ClassVar as _ClassVar,
)


class _NodeMixinSortMeta(type):
    """Node metaclass for initializing `Node` subclass after other `mixin` classes"""

    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, object]):
        def sorter(base: type) -> bool:
            return isinstance(base, Node)

        sorted_bases = tuple(sorted(bases, key=sorter))
        new_type = super().__new__(cls, name, sorted_bases, attrs)
        return new_type


class Node(metaclass=_NodeMixinSortMeta):
    _queued_nodes: _ClassVar[list[Node]] = []
    _uid_counter: _ClassVar[_count] = _count(0, 1)
    node_instances: _ClassVar[dict[int, Node]] = {}

    def __new__(cls, *args: _Any, **kwargs: _Any):
        instance = super().__new__(cls, *args, **kwargs)
        instance.uid = next(Node._uid_counter)
        Node.node_instances[instance.uid] = instance
        return instance

    uid: int  # is set in `Node.__new__`
    parent: Node | None = None
    process_priority: int = 0

    def with_parent(self, parent: Node | None, /):
        self.parent = parent
        return self

    def with_process_priority(self, process_priority: int, /):
        self.process_priority = process_priority
        return self

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(#{self.uid})"

    def update(self, delta: float) -> None: ...

    def queue_free(self) -> None:
        Node._queued_nodes.append(self)

    def free(self) -> None:
        del Node.node_instances[self.uid]
