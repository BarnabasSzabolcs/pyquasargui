from quasargui.base import Component, ComponentWithModel
from quasargui.model import Model
from quasargui.tools import build_props
from quasargui.typing import ClassesType, StylesType, PropsType, EventsType, PropValueType


class Input(ComponentWithModel):
    component = 'q-input'

    def __init__(self,
                 label: str = None,
                 value: str = None,
                 model: Model = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        props = build_props({}, props, {'label': label})
        super().__init__(model=model, value=value, classes=classes, styles=styles, props=props, events=events)


class Button(Component):
    component = 'q-btn'
    defaults = {
        'props': {
            'unelevated': True,
        }
    }

    def __init__(self,
                 label: str = None,
                 icon: str = None,
                 color: PropValueType[str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        props = build_props(self.defaults['props'], props, {
            'label': label,
            'icon': icon,
            'color': color})
        super().__init__(classes=classes, styles=styles, props=props, events=events)


class Toggle(ComponentWithModel):
    """
    ref. https://quasar.dev/vue-components/toggle#qtoggle-api
    """
    component = 'q-toggle'

    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        props = build_props({}, props, {
            'label': label})
        super().__init__(model=model, classes=classes, styles=styles, props=props, events=events)
