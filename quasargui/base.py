import os
import textwrap
from inspect import signature
from typing import Optional, TYPE_CHECKING, Dict, Callable, Union, List

from quasargui.model import Renderable, Reactive, Model, PropVar
from quasargui.tools import build_props, merge_classes
from quasargui.typing import ChildrenType, ClassesType, StylesType, PropsType, EventsType, PropValueType, EventCBType

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

    @classmethod
    def render_cb(cls, cb: EventCBType):
        return cls.register(cb) if isinstance(cb, Callable) else cb.render_as_data()

    @classmethod
    def render_events(cls, events: EventsType):
        return {
            event: cls.render_cb(cb)
            for event, cb in events.items()
        }


class JSRaw(Renderable):
    def __init__(self, code: str):
        if '"' in code:
            raise AssertionError('JSFunction code cannot contain \'"\'.')
        self.code = textwrap.dedent(code)

    def render_as_data(self) -> dict:
        return {'$': self.code}

    @property
    def js_var_name(self) -> str:
        return self.code


class Component:
    """
    A renderable GUI component.
    """
    max_id = 0
    component = 'div'
    defaults = {}
    script_sources: List[str] = []
    style_sources: List[str] = []
    render_children_immediately: bool = False

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
        self._events = EventCallbacks.render_events(events or {})
        self._children = children or []
        self.api: Optional['Api'] = None
        # other objects that should be attached to the api when this Component is attached:
        self.dependents: List[Union[Component, Reactive, Callable[['Api'], None]]] = []
        Component.max_id += 1
        self.id = Component.max_id

    @property
    def vue(self) -> dict:
        props = {
            k: v.render_as_data() if isinstance(v, Renderable) else v
            for k, v in self.props.items()
        }
        classes = self.classes if isinstance(self.classes, str) else " ".join(cs for cs in self.classes)
        styles = ";".join('{k}:{v}'.format(k=k, v=v) for k, v in self.styles.items())
        if styles:
            props.update({'style': styles})
        result = {}
        if hasattr(self, '_prop_var'):
            result['arg'] = self._prop_var.js_var_name
        children = self._children

        slots = {slot.name: slot.vue for slot in children if isinstance(slot, Slot)}
        slots = {name: value for name, value in slots.items() if len(value['children'])}
        try:
            result.update({
                'id': self.id,
                'component': getattr(self, 'component', None),
                'events': self._events,
                'props': props,
                'classes': classes,
                'children': [child if isinstance(child, str) else
                             child.render_mustache() if isinstance(child, Renderable) else
                             child.vue
                             for child in children if not isinstance(child, Slot)],
                'slots': slots,
                'recursive': self.render_children_immediately
            })
        except AttributeError as e:
            wrong_children = [child for child in children if
                              not (isinstance(child, str) or
                                   isinstance(child, Renderable) or
                                   isinstance(child, Component))]
            if wrong_children:
                type_children = [child for child in wrong_children if isinstance(child, type)]
                if type_children:
                    raise AssertionError(
                        "{children} should be not a type but an object (Did you forget to add '()'?)".format(
                            children=', '.join(str(child) for child in type_children)))
            else:
                raise e
        return result

    def _merge_vue(self, d: dict) -> dict:
        # ref. https://stackoverflow.com/a/1021484/1031191
        # noinspection PyArgumentList
        d_base = {k: v for k, v in Component.vue.fget(self).items()}
        d_base.update(d)
        return d_base

    def set_api(self, api: 'Api', _flush: bool = True):
        self.api = api
        if self.script_sources:
            self.api.import_scripts(self.script_sources)
        if self.style_sources:
            self.api.import_styles(self.style_sources)
        for child in self._children:
            if hasattr(child, 'set_api'):
                child.set_api(api, _flush=False)
        for dependent in self.dependents:
            if isinstance(dependent, Callable):
                dependent(api)
            else:
                dependent.set_api(api, _flush=False)
        for prop in self.props.values():
            if isinstance(prop, Reactive):
                prop.set_api(api, _flush=False)
        if _flush:
            api.flush_model_data()

    def remove_api(self):
        self.api = None
        for child in self._children:
            if hasattr(child, 'remove_api'):
                child.remove_api()
        for dependent in self.dependents:
            if not isinstance(dependent, Callable):
                dependent.remove_api()
        for prop in self.props.values():
            if isinstance(prop, Reactive):
                prop.remove_api()

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

    def add_event(self, event: str, cb: EventCBType):
        self._events[event] = EventCallbacks.render_cb(cb)

    def notify(self, message: str, **params):
        self.api.plugins.notify(message, **params)


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
        props['v-model'] = self._model
        super().__init__(children=children,
                         classes=classes,
                         styles=styles,
                         props=props,
                         events=events)
        self.dependents.append(self._model)

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
    """
    Represents a vue v-slot, to be used in children parameter of a Component.

    To access scoped slots,
    ::

        Component(children=[
            Slot('name', lambda prop: [... children ...])
        ])

    prop is a PropVar that behaves similarly to a Model.

    To access default slot, set name = 'default' (or '').
    """
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


class SingleFileComponent(Component):
    """
    Extend this component to add your external component, written in .vue.
    ::

        class YourSFC(SingleFileComponent):
            vue_source = 'path/to/your.vue'

    **Note:** the SFC support is limited (it does not handle imports and styles other than css).

    If you want to import a more serious vue component,

    1. compile your source into .umd.js
    2. create your class like the following:

    ::

        class YourComponentName(Component):
            script_source = ['path/to/your.umd.js']
            component = 'your-component-name'

        class YourOtherComponentName(Component):
            script_source = ['path/to/your.umd.js']
            component = 'your-other-component-name'

    Any script that is included with ``script_source`` is only included once in the HTML source of the GUI.
    """
    vue_source: str = ''  # override this with your .vue path
    component = None

    def __init__(self,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        if not isinstance(self.__class__.vue_source, str):
            raise TypeError('vue_source must be str')
        if self.__class__.component is None:
            component_name = self.vue_source.split(os.path.sep)[-1].rsplit('.vue', 1)[0]
            self.__class__.component = component_name

        super().__init__(
            children=children,
            classes=classes,
            styles=styles,
            props=props,
            events=events
        )
        self.dependents.append(
            lambda api:
                api.register_sfc(self.__class__.component, self.vue_source))
