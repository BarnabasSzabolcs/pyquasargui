import textwrap
from inspect import signature
from typing import Optional, TYPE_CHECKING, Dict, Callable, Union, List

from quasargui.model import Renderable, Reactive, Model, PropVar
from quasargui.tools import build_props, merge_classes
from quasargui.typing import ChildrenType, ClassesType, StylesType, PropsType, EventsType, PropValueType

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
        self.code = textwrap.dedent(code)

    def render_as_data(self) -> dict:
        return {'$': self.code}

    def js_var_name(self) -> str:
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
        self.styles = build_props(self.defaults.get('styles', {}), styles or {})
        if not hasattr(self, 'props'):
            self.props = build_props(self.defaults.get('props', {}), props or {})
        events = events or {}
        self.events = {event: EventCallbacks.register(cb) if isinstance(cb, Callable) else cb.render_as_data()
                       for event, cb in events.items()}
        self._children = children or []
        self.api: Optional['Api'] = None
        # other objects that should be attached to the api when this Component is attached:
        self.dependents: List[Union[Component, Reactive]] = []
        Component.max_id += 1
        self.id = Component.max_id

    @property
    def vue(self) -> dict:
        props = {
            k: v.render_as_data() if isinstance(v, Renderable) else v
            for k, v in self.props.items()
        }
        classes = self.classes if isinstance(self.classes, str) else " ".join(cs for cs in self.classes)
        if classes:
            props.update({'class': classes})
        styles = ";".join('{k}:{v}'.format(k=k, v=v) for k, v in self.styles.items())
        if styles:
            props.update({'style': styles})
        result = {}
        if hasattr(self, '_prop_var'):
            result['arg'] = self._prop_var.js_var_name
        children = self._children
        if any([isinstance(child, type) for child in children]):
            raise AssertionError(
                "{children} should be not a type but an object (Did you forget to add '()'?)".format(
                    children=', '.join(str(child) for child in children if isinstance(child, type))))

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
        self.api = api
        if hasattr(self, 'script_sources'):
            self.api.import_scripts(self.script_sources)
        if hasattr(self, 'style_sources'):
            self.api.import_styles(self.style_sources)
        for child in self._children:
            if hasattr(child, 'set_api'):
                child.set_api(api, _flush=False)
        for dependent in self.dependents:
            dependent.set_api(api, _flush=False)
        for prop in self.props.values():
            if isinstance(prop, Reactive):
                prop.set_api(api, _flush=False)
        if _flush:
            api.flush_model_data()

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
                if hasattr(child, 'set_api'):
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


class LabeledComponent(ComponentWithModel):
    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: ChildrenType = None):
        props = build_props({}, props, {'label': label})
        super().__init__(model=model, classes=classes, styles=styles, props=props, events=events, children=children)


class Slot(Component):
    component = 'template'

    def __init__(self,
                 name: str,
                 children: Union[ChildrenType, Callable[[PropVar], ChildrenType]] = None,
                 props: PropsType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None):
        self.name = name
        if isinstance(children, Callable):
            prop_var = PropVar()
            children = children(prop_var)
            self._prop_var = prop_var
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


def v_for(
        model: Union[Renderable, list, dict],
        component: Union[
            Callable[[PropVar], Component],
            Callable[[PropVar, PropVar], Component]
        ] = None,
        key: PropValueType[str] = None
) -> Component:

    if not isinstance(model, Renderable):
        model = Model(model)
    model_js = model.js_var_name
    n_args = len(signature(component).parameters)
    if n_args == 1:
        p1 = PropVar()
        component = component(p1)
        component.props['v-for'] = JSRaw("{} in {}".format(
            p1.js_var_name, model_js))
        if key is None:
            key = 'index'
    elif n_args == 2:
        p1, p2 = PropVar(), PropVar()
        component = component(p1, p2)
        component.props['v-for'] = JSRaw("({}, {}) in {}".format(
            p1.js_var_name, p2.js_var_name, model_js))
    else:
        raise AssertionError
    if key is not None:
        component.props['key'] = key
    if isinstance(model, Reactive):
        component.dependents.append(model)
    return component


def v_show(
    condition: Reactive,
    component: Component
) -> Component:
    _set_prop_safe(component, 'v-show', condition)
    return component


def v_if(
    condition: Reactive,
    component: Component
) -> Component:
    _set_prop_safe(component, 'v-if', condition)
    return component


def v_else(
    component: Component
) -> Component:
    _set_prop_safe(component, 'v-else', None)
    return component


def v_else_if(
    condition: Reactive,
    component: Component
) -> Component:
    _set_prop_safe(component, 'v-else-if', condition)
    return component


def v_once(component: Component) -> Component:
    """
    This directive is rarely used.
    ref. https://v3.vuejs.org/api/directives.html#v-once
    """
    _set_prop_safe(component, 'v-once', None)
    return component


def v_pre(component: Component) -> Component:
    """
    This directive is rarely used.
    It enables displaying raw mustache tags.
    ref. https://v3.vuejs.org/api/directives.html#v-pre
    """
    _set_prop_safe(component, 'v-pre', None)
    return component


# v_cloak is not necessary since all the components are loaded after Vue is loaded.


def _set_prop_safe(component, prop_name, prop_value) -> None:
    if prop_name in component.props:
        raise AssertionError("When using {}, don't define '{}' prop.".format(
            prop_name.replace('-', '_'), prop_name))
    component.props[prop_name] = prop_value


def v_html(
        value: PropValueType[str],
        component: Component
) -> Component:
    if component.children:
        raise AssertionError("Don't set children when using v_html.")
    _set_prop_safe(component, 'v-html', value)
    return component
