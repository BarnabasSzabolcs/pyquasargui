from typing import Dict, Callable, Any, List, Union, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from ._base import Model
    # noinspection PyUnresolvedReferences
    from .components import Component

EventsType = Dict[str, Callable[[...], Any]]
ClassesType = str
StylesType = Dict[str, str]

ChildrenType = List[Union['Component', str, 'Model']]
ValueType = Union[bool, int, float, str, list, dict, None]

T = TypeVar('T')
PropValueType = Union[T, 'Model']
PropsType = Dict[str, PropValueType[ValueType]]
