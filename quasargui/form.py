from typing import List

from quasargui.base import Component, ComponentWithModel, Slot
from quasargui.model import Model
from quasargui.tools import build_props
from quasargui.typing import ClassesType, StylesType, PropsType, EventsType, PropValueType, ChildrenType


class Input(ComponentWithModel):
    """
    ref. https://quasar.dev/vue-components/input#qinput-api
    """
    component = 'q-input'
    defaults = {'props': {}}

    # noinspection PyShadowingBuiltins
    def __init__(self,
                 label: str = None,
                 value: str = None,
                 model: Model = None,
                 type: PropValueType[str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: List[Slot] = None):
        props = build_props(self.defaults['props'], props, {
            'label': label,
            'type': type,
        })
        if props.get('type', '') == 'number':
            model = model or Model('')
            model.modifiers.add('number')
        used_slots = {slot.name for slot in children or []}
        bottom_slots = {'error', 'hint', 'counter'}
        bottom_slots_used = used_slots & bottom_slots
        if bottom_slots_used and 'bottom-slots' not in props:
            props['bottom-slots'] = True
        if 'label' in used_slots and 'label-slot' not in props:
            props['label-slot'] = True
        super().__init__(
            model=model,
            value=value,
            classes=classes,
            styles=styles,
            props=props,
            events=events,
            children=children)


class Button(Component):
    """
    ref. https://quasar.dev/vue-components/button#qbtn-api
    """
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
                 events: EventsType = None,
                 children: ChildrenType = None):
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
    defaults = {'props': {}}

    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: ChildrenType = None):
        props = build_props(self.defaults['props'], props, {
            'label': label})
        super().__init__(model=model, classes=classes, styles=styles, props=props, events=events, children=children)
