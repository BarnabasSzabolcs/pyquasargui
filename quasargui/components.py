from typing import List, Dict, Callable, Any, Union, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .main import Api

EventsType = Dict[str, Callable[[...], Any]]
ClassesType = Union[str, List[str]]
StylesType = Dict[str, str]
PropsType = Dict[str, Any]
ChildrenType = List['Component']


class Data:
    """
    Data is all the data that can change
    in both the GUI and on the backend
    (typically the value of an Input)
    """
    max_id = 1
    data_dic = {}

    def __init__(self, value):
        self.id = str(Data.max_id)
        Data.max_id += 1
        self.data_dic[self.id] = self
        self._value = value
        self.api = None

    def __del__(self):
        del self.data_dic[self.id]

    def set_api(self, api: 'Api'):
        self.api = api
        self.api.set_data(self.id, self._value)

    @property
    def value(self) -> str:
        if self.api is not None:
            return self.api.get_data(self.id)
        else:
            return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.api.set_data(self.id, self._value)

    def render(self):
        return {'@': self.id, 'value': self.value}


class EventCallbacks:
    """
    This is a namespace, not a class.
    """
    callbacks: Dict[int, Callable] = {}
    max_id: int = 0

    @classmethod
    def register(cls, cb):
        cb_id = cls.max_id
        cls.callbacks[cb_id] = cb
        cls.max_id += 1
        return cb_id

    @classmethod
    def get(cls, cb_id: int):
        return cls.callbacks[cb_id]

    @classmethod
    def remove(cls, cb_id: int):
        del cls.callbacks[cb_id]


class Component:
    """
    A renderable GUI component.
    """
    max_id = 0

    def __init__(self,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: ChildrenType = None):
        self.classes = classes or {}
        self.styles = styles or {}
        self.props = props or {}
        events = events or {}
        self.events = {event: EventCallbacks.register(cb)
                       for event, cb in events.items()}
        self.children = children or []
        self.api: Optional[Api] = None
        Component.max_id += 1
        self.id = Component.max_id

    @property
    def vue(self) -> dict:
        props = {k: v for k, v in self.props.items()}
        classes = self.classes if isinstance(self.classes, str) else " ".join(cs for cs in self.classes)
        if classes:
            props.update({'class': classes})
        styles = ";".join(f'{k}:{v}' for k, v in self.styles.items())
        if styles:
            props.update({'style': styles})
        return {
            'events': self.events,
            'props': props,
            'children': [child if isinstance(child, str) else child.vue for child in self.children]
        }

    def _merge_vue(self, d: dict) -> dict:
        # ref. https://stackoverflow.com/a/1021484/1031191
        # noinspection PyArgumentList
        d_base = {k: v for k, v in Component.vue.fget(self).items()}
        d_base.update(d)
        return d_base

    def set_api(self, api: 'Api'):
        # noinspection PyAttributeOutsideInit
        self.api = api
        for child in self.children:
            if isinstance(child, Component):
                child.set_api(self.api)

    def notify(self, message: str):
        self.api.send_notification(message)


class Layout(Component):
    def __init__(self,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: ChildrenType = None):
        super().__init__(classes, styles, props, events, children)

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'div'
        })


class Input(Component):
    def __init__(self,
                 value: str = '',
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        self._value_ref = Data(value)
        props = props or {}
        props['value'] = self._value_ref.render()
        super().__init__(classes, styles, props, events)

    def set_api(self, api: 'Api'):
        super().set_api(api)
        self._value_ref.set_api(api)

    @property
    def value(self):
        return self._value_ref.value

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-input',
        })


class Button(Component):
    def __init__(self,
                 label: str = '',
                 icon: str = '',
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        props = props or {}
        if label and 'label' not in props:
            props['label'] = label
        if icon and 'icon' not in props:
            props['icon'] = icon
        super().__init__(classes, styles, props, events)

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-btn'
        })