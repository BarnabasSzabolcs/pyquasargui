from typing import Dict, Callable, TYPE_CHECKING, Optional

from .typing import EventsType, ClassesType, StylesType, PropsType, ChildrenType, ValueType

if TYPE_CHECKING:
    from .main import Api


class Model:
    """
    Data is all the data that can change
    in both the GUI and on the backend
    (typically the value of an Input)
    """
    max_id = 1
    data_dic = {}

    def __init__(self, value):
        self.id = Model.max_id
        Model.max_id += 1
        self.data_dic[self.id] = self
        self._value = value
        self.api = None

    def __del__(self):
        del self.data_dic[self.id]

    def set_api(self, api: 'Api'):
        if self.api != api:
            self.api = api
            api.set_data(self.id, self._value)

    @property
    def value(self) -> str:
        if self.api is not None:
            return self.api.get_data(self.id)
        else:
            return self._value

    @value.setter
    def value(self, value):
        if self._value == value:
            return
        self._value = value
        if self.api is not None:
            self.api.set_data(self.id, self._value)

    def render(self):
        return {'@': self.id, 'value': self.value}

    def render_mustache(self) -> str:
        return "{{$root.data[" + str(self.id) + "]}}"


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
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        self.classes = classes or ''
        self.styles = styles or {}
        self.props = props or {}
        events = events or {}
        self.events = {event: EventCallbacks.register(cb)
                       for event, cb in events.items()}
        self._children = children or []
        self.api: Optional['Api'] = None
        Component.max_id += 1
        self.id = Component.max_id
        self.dependent_models = [v for v in self.props.values() if isinstance(v, Model)]

    @property
    def vue(self) -> dict:
        props = {
            k: v.render() if isinstance(v, Model) else v
            for k, v in self.props.items()
        }
        classes = self.classes if isinstance(self.classes, str) else " ".join(cs for cs in self.classes)
        if classes:
            props.update({'class': classes})
        styles = ";".join('{k}:{v}'.format(k=k, v=v) for k, v in self.styles.items())
        if styles:
            props.update({'style': styles})
        return {
            'id': self.id,
            'events': self.events,
            'props': props,
            'children': [child if isinstance(child, str) else
                         child.render_mustache() if isinstance(child, Model)
                         else child.vue
                         for child in self._children]
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
        for child in self._children:
            if isinstance(child, Component):
                child.set_api(api)
        for model in self.dependent_models:
            model.set_api(api)

    def notify(self, message: str, **kwargs):
        params = {'message': message}
        if kwargs:
            params.update(kwargs)
        self.api.send_notification(params)

    @property
    def children(self):
        return self._children

    def set_children(self, children: ChildrenType):
        self._children = children
        if self.api is not None:
            for child in children:
                if isinstance(child, Component):
                    child.set_api(self.api)
            self.api.set_component(self.vue)


class ComponentWithModel(Component):
    def __init__(self,
                 model: Optional[Model],
                 value: ValueType = None,
                 children: Component = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        if model is not None and value is not None:
            raise AssertionError("Cannot set both model and value.")
        value = value or ''
        self._model = model or Model(value)
        props = props or {}
        props['value'] = self._model.render()
        super().__init__(children=children,
                         classes=classes,
                         styles=styles,
                         props=props,
                         events=events)

    def set_api(self, api: 'Api'):
        super().set_api(api)
        self._model.set_api(api)

    @property
    def model(self):
        return self._model

    @property
    def value(self):
        return self._model.value

    @value.setter
    def value(self, value):
        self._model.value = value