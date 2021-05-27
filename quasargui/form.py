from quasargui.base import *
from quasargui.base import Component
from quasargui.tools import build_props
from quasargui.typing import *


class Input(ComponentWithModel):
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

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-input',
        })


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
