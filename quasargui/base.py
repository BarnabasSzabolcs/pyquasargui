from typing import Optional, TYPE_CHECKING, Dict, Callable, Union

from quasargui.model import Renderable, Reactive, Model, PropVar
from quasargui.tools import build_props, merge_classes
from quasargui.typing import ChildrenType, ClassesType, StylesType, PropsType, EventsType

if TYPE_CHECKING:
    from quasargui.main import Api


class EventCallbacks:
    """
    This is a namespace, not a class.
    """
    callbacks: Dict[int, Callable] = {}
    max_id: int = 0

    @classmethod
    def register(cls, cb):
        cls.max_id += 1
        cb_id = cls.max_id
        cls.callbacks[cb_id] = cb
        return cb_id

    @classmethod
    def get(cls, cb_id: int):
        return cls.callbacks[cb_id]

    @classmethod
    def remove(cls, cb_id: int):
        del cls.callbacks[cb_id]


class JSRaw(Renderable):
    def __init__(self, code: str):
        if '"' in code:
            raise AssertionError('JSFunction code cannot contain \'"\'.')
        self.code = code

    def render_as_data(self) -> dict:
        return {'$': self.code}

    def render_mustache(self) -> str:
        return self.code


class Component:
    """
    A renderable GUI component.
    """
    max_id = 0
    defaults = {}

    def __init__(self,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        if not hasattr(self, 'classes'):
            self.classes = merge_classes(self.defaults.get('classes', ''), classes or '')
        self.styles = styles or {}
        if not hasattr(self, 'props'):
            self.props = build_props(self.defaults.get('props', {}), props or {})
        events = events or {}
        self.events = {event: EventCallbacks.register(cb)
                       for event, cb in events.items()}
        self._children = children or []
        self.api: Optional['Api'] = None
        Component.max_id += 1
        self.id = Component.max_id

    @property
    def vue(self) -> dict:
        props = {
            k: v.render_as_data() if isinstance(v, Renderable) or isinstance(v, JSRaw) else v
            for k, v in self.props.items()
        }
        classes = self.classes if isinstance(self.classes, str) else " ".join(cs for cs in self.classes)
        if classes:
            props.update({'class': classes})
        styles = ";".join('{k}:{v}'.format(k=k, v=v) for k, v in self.styles.items())
        if styles:
            props.update({'style': styles})
        result = {}
        if isinstance(self._children, Callable):
            propVar = PropVar()
            children = self._children(propVar)
            result['arg'] = propVar.js_var_name
        else:
            children = self._children
        slots = {slot.name: slot.vue for slot in children if isinstance(slot, Slot)}
        slots = {name: value for name, value in slots.items() if len(value['children'])}
        result.update({
            'id': self.id,
            'component': getattr(self, 'component', None),
            'events': self.events,
            'props': props,
            'children': [child if isinstance(child, str) else
                         child.render_mustache() if isinstance(child, Renderable) else
                         child.vue
                         for child in children if not isinstance(child, Slot)],
            'slots': slots
        })
        return result

    def _merge_vue(self, d: dict) -> dict:
        # ref. https://stackoverflow.com/a/1021484/1031191
        # noinspection PyArgumentList
        d_base = {k: v for k, v in Component.vue.fget(self).items()}
        d_base.update(d)
        return d_base

    def set_api(self, api: 'Api', _flush: bool = True):
        # noinspection PyAttributeOutsideInit
        self.api = api
        if isinstance(self._children, list):
            for child in self._children:
                if isinstance(child, Component) or isinstance(child, Reactive):
                    child.set_api(api, _flush=False)
        for prop in self.props.values():
            if isinstance(prop, Reactive):
                prop.set_api(api, _flush=False)
        if _flush:
            api.flush_data()

    def notify(self, message: str, **kwargs):
        params = {'message': message}
        if kwargs:
            params.update(kwargs)
        self.api.show_notification(**params)

    @property
    def children(self):
        return self._children

    def set_children(self, children: ChildrenType):
        self._children = children
        if self.api is not None:
            for child in children:
                if isinstance(child, Component):
                    child.set_api(self.api)
            self.update()

    def update(self):
        if self.api is not None:
            self.api.set_component(self.vue)


class ComponentWithModel(Component):
    def __init__(self,
                 model: Renderable = None,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        self._model = model or Model(None)
        props = props or {}
        props['value'] = self._model.render_as_data()
        super().__init__(children=children,
                         classes=classes,
                         styles=styles,
                         props=props,
                         events=events)

    def set_api(self, api: 'Api', _flush: bool = True):
        super().set_api(api, _flush=_flush)
        self._model.set_api(api, _flush=_flush)

    @property
    def model(self):
        return self._model

    @property
    def value(self):
        return self._model.value

    @value.setter
    def value(self, value):
        if not isinstance(self._model, Model):
            raise AssertionError('Cannot change value if instance\'s value is not Model')
        self._model.value = value


class Slot(Component):
    component = 'template'

    def __init__(self,
                 name: str,
                 children: Union[ChildrenType, Callable[[PropVar], ChildrenType]] = None,
                 props: PropsType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None):
        self.name = name
        super().__init__(props=props, children=children, classes=classes, styles=styles)


class RemoveSlot(Slot):
    """
    Removes a previously defined slot from within a Component's children.
    """
    component = 'template'

    def __init__(self, name: str):
        super().__init__(name)


class CustomComponent(Component):
    """
    Use this with html tags and custom components.
    """
    def __init__(self,
                 component: str = None,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        self.component = component
        super().__init__(
            children=children,
            classes=classes,
            styles=styles,
            props=props,
            events=events
        )
