from __future__ import annotations as _annotations

# ==( Custom Annotations )==
# This file contains private annotations used across this package.
# Whenever there is a "?" comment, it means that
# a type may or may not implement that field or mixin class.

from typing import (
    TypeVar as _TypeVar,
    Protocol as _Protocol,
    ClassVar as _ClassVar,
    Any as _Any,
    TYPE_CHECKING as _TYPE_CHECKING,
)

from linflex import (
    Vec2 as _Vec2,
    Vec2i as _Vec2i,
)
from colex import ColorValue as _ColorValue
from typing_extensions import Self as _Self

if _TYPE_CHECKING:
    from ._clock import DeltaClock as _DeltaClock
    from ._screen import Screen as _Screen
    from ._components._animation import (
        Animation as _Animation,
        AnimationMapping as _AnimationMapping,
    )

EngineType = _TypeVar("EngineType", bound="Engine", covariant=True)
NodeType = _TypeVar("NodeType", bound="Node", covariant=True)
T = _TypeVar("T")
_T_contra = _TypeVar("_T_contra", contravariant=True)


class FileLike(_Protocol[_T_contra]):
    def write(self, stream: _T_contra, /) -> object: ...
    def flush(self, /) -> None: ...
    def fileno(self, /) -> int: ...


class Engine(_Protocol):
    fps: float
    clock: _DeltaClock
    screen: _Screen
    is_running: bool


class Node(_Protocol):
    node_instances: _ClassVar[dict[int, Node]]
    uid: int

    def __init__(self) -> None: ...
    def with_parent(self: _Self, parent: Node | None, /) -> _Self: ...
    def with_process_priority(self, process_priority: int, /) -> _Self: ...
    def update(self, delta: float) -> None: ...
    def queue_free(self) -> None: ...
    def free(self) -> None: ...


class TransformComponent(_Protocol):
    transform_instances: _ClassVar[dict[int, TransformNode]]
    position: _Vec2
    rotation: float
    z_index: int
    top_level: bool

    def with_position(
        self: _Self,
        position: _Vec2 | None = None,
        /,
        x: float | None = None,
        y: float | None = None,
    ) -> _Self: ...
    def with_global_position(
        self: _Self,
        global_position: _Vec2 | None = None,
        /,
        x: float | None = None,
        y: float | None = None,
    ) -> _Self: ...
    def with_rotation(self: _Self, rotation: float, /) -> _Self: ...
    def with_global_rotation(self: _Self, global_rotation: float, /) -> _Self: ...
    def with_z_index(self: _Self, z_index: int, /) -> _Self: ...
    def as_top_level(self: _Self, state: bool = True, /) -> _Self: ...
    @property
    def global_position(self) -> _Vec2: ...
    @global_position.setter
    def global_position(self, position: _Vec2) -> None: ...
    @property
    def global_rotation(self) -> float: ...
    @global_rotation.setter
    def global_rotation(self, rotation: float) -> None: ...


class TransformNode(
    TransformComponent,
    Node,
    _Protocol,
): ...


class TextureComponent(_Protocol):
    texture_instances: _ClassVar[dict[int, TextureNode]]
    texture: list[str]
    visible: bool
    centered: bool
    transparency: str | None

    def with_texture(self: _Self, texture_or_line: list[str] | str, /) -> _Self: ...
    def as_visible(self: _Self, state: bool = True, /) -> _Self: ...
    def as_centered(self: _Self, state: bool = True, /) -> _Self: ...
    def with_transparency(self: _Self, state: bool = True, /) -> _Self: ...
    def hide(self) -> None: ...
    def show(self) -> None: ...
    def is_globally_visible(self) -> bool: ...
    def get_texture_size(self) -> _Vec2i: ...


class TextureNode(
    TextureComponent,
    TransformComponent,
    Node,
    _Protocol,
): ...


class ColorComponent(_Protocol):
    color_instances: _ClassVar[dict[int, ColorNode]]
    color: _ColorValue | None

    def with_color(
        self: _Self,
        color: _ColorValue | None,
        /,
    ) -> _Self: ...


class ColorNode(
    ColorComponent,
    TextureComponent,
    TransformNode,
    Node,
    _Protocol,
): ...


class Renderable(  # possible base: `ColorComponent`
    TextureComponent,
    TransformComponent,
    Node,
    _Protocol,
):
    ...
    # possible field: `color` of type `_ColorValue`


class AnimatedComponent(_Protocol):
    animated_instances: _ClassVar[dict[int, AnimatedNode]]
    animations: _AnimationMapping
    current_animation: _Animation | None = None
    _frame_index: int = 0

    def with_animations(self: _Self, animations: dict[str, _Any], /) -> _Self: ...
    def with_animation(
        self: _Self,
        animation_name: str,
        animation: _Animation,
        /,
    ) -> _Self: ...
    def add_animation(
        self,
        animation_name: str,
        animation: _Animation,
    ) -> None: ...
    def play(self, animation_name: str, /) -> None: ...
    def _wrapped_update_animated(self, _delta: float) -> None: ...


class AnimatedNode(  # possible base: `ColorComponent`
    AnimatedComponent,
    TextureComponent,
    TransformComponent,
    Node,
    _Protocol,
):
    ...
    # possible field: `color` of type `_ColorValue`
