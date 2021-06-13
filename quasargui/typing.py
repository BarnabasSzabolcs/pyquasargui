from typing import Dict, Callable, Any, List, Union, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from quasargui.base import JSRaw
    # noinspection PyUnresolvedReferences
    from quasargui.model import Model, Reactive
    # noinspection PyUnresolvedReferences
    from quasargui.components import Component

EventsType = Dict[str, Union[Callable[[...], Any], 'JSRaw']]
ClassesType = str
StylesType = Dict[str, str]

ChildrenType = List[Union['Component', str, 'Reactive']]
ValueType = Union[bool, int, float, str, list, dict, None]
PathSegmentType = Union[str, int]
PathType = List[PathSegmentType]

T = TypeVar('T')
PropValueType = Union[T, 'Reactive']
PropsType = Dict[str, PropValueType[ValueType]]
