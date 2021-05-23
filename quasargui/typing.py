from typing import Dict, Callable, Any, List, Union

EventsType = Dict[str, Callable[[...], Any]]
ClassesType = str
StylesType = Dict[str, str]
PropsType = Dict[str, Any]
ChildrenType = List[Union['Component', str, 'Model']]
ValueType = Union[bool, int, float, str, list, dict, None]
