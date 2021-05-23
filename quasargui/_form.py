from typing import Union

from quasargui._base import ComponentWithModel, Component, Model
from quasargui._tools import build_props
from quasargui.typing import ClassesType, StylesType, PropsType, EventsType


class Input(ComponentWithModel):
    def __init__(self,
                 value: str = None,
                 model: Model = None,
                 label: str = None,
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
    defaults = {
        'props': {
            'unelevated': True,
        }
    }

    def __init__(self,
                 label: str = None,
                 icon: str = None,
                 color: Union[Model, str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        props = build_props(self.defaults['props'], props, {
            'label': label,
            'icon': icon,
            'color': color})
        super().__init__(classes=classes, styles=styles, props=props, events=events)

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-btn'
        })