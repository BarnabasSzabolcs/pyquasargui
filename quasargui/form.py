from typing import List, Type, Union

from quasargui.base import Component, ComponentWithModel, Slot
from quasargui.components import Div
from quasargui.model import Model
from quasargui.tools import build_props, merge_classes
from quasargui.typing import ClassesType, StylesType, PropsType, EventsType, PropValueType, ChildrenType


class Form(Component):
    component = 'form'
    defaults = {'classes': 'q-gutter-md'}

    def __init__(self,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 events: EventsType = None,
                 ):
        super().__init__(children=children, classes=classes, styles=styles, events=events)


class Input(ComponentWithModel):
    """
    ref. https://quasar.dev/vue-components/input#qinput-api
    """
    component = 'q-input'
    defaults = {'props': {}}

    # noinspection PyShadowingBuiltins
    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 type: PropValueType[str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: List[Slot] = None):
        props = build_props({}, props, {
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
            classes=classes,
            styles=styles,
            props=props,
            events=events,
            children=children)

    def validate(self):
        return self.api.call_component_method(self.id, 'validate')

    def reset_validation(self):
        return self.api.call_component_method(self.id, 'resetValidation')


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

    # noinspection PyShadowingBuiltins
    def __init__(self,
                 label: PropValueType[str] = None,
                 icon: PropValueType[str] = None,
                 color: PropValueType[str] = None,
                 type: PropValueType[str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: ChildrenType = None):
        props = build_props({}, props, {
            'label': label,
            'icon': icon,
            'color': color,
            'type': type
        })
        super().__init__(classes=classes, styles=styles, props=props, events=events, children=children)


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
        props = build_props({}, props, {'label': label})
        super().__init__(model=model, classes=classes, styles=styles, props=props, events=events, children=children)


class Knob(ComponentWithModel):
    component = 'q-knob'
    defaults = {
        'props': {
            'track-color': 'grey-3',
            'color': 'primary',
            'unelevated': True,
            'show-value': True
        }
    }


class Slider(ComponentWithModel):
    component = 'q-slider'
    defaults = {
        'props': {
            'label': True
        }
    }


class InputStr(Input):
    """This is just an alias for completeness"""


class _NumericInput(ComponentWithModel):
    _type: Type = None
    defaults = {
        'field_classes': 'text-sm',
        'control_props': {'snap': True}
    }

    # noinspection PyShadowingBuiltins
    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 appearance: str = None,
                 min: Union[int, float] = None,
                 max: Union[int, float] = None,
                 props: PropsType = None,
                 field_props: PropsType = None,
                 field_classes: ClassesType = None,
                 field_styles: StylesType = None,
                 children: List[Slot] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 events: EventsType = None):
        appearance = appearance or 'input'
        self.component = {
            'input': 'q-input',
            'knob': 'q-field',
            'slider': 'q-field'
        }[appearance]
        model = model or Model(0, self._type)
        model.modifiers.add('number')
        model._type = self._type
        special_props = {
            'min': min,
            'max': max
        }

        if appearance in {'knob', 'slider'}:
            component_class = {'knob': Knob, 'slider': Slider}[appearance]
            control_props = build_props(self.defaults['control_props'], props)
            control_props = build_props({
                'label-position': 'before' if appearance == 'knob' else 'top'
            }, control_props, special_props)
            control = component_class(
                model=model,
                props=control_props,
                children=children,
                classes=classes,
                styles=styles,
                events=events,
            )
            label_position = control_props['label-position']

            field_props = build_props({
                'borderless': True,
                'stack-label': True,
            }, field_props, {'label': label if label_position == 'top' else None})
            label_slot = []
            if label and label_position != 'top':
                field_classes = merge_classes(self.defaults['field_classes'], field_classes or '')
                if isinstance(label, str):
                    label = Div([label], classes=field_classes)
                label_position = {
                    'left': 'before',
                    'right': 'after'
                }.get(label_position, label_position)
                label_slot = [Slot(label_position, children=[label])]
            super().__init__(
                model=model,
                props=field_props,
                children=[Slot('control', [control])] + label_slot
            )
        else:
            props = build_props({'type': 'number'}, props, special_props)
            props = build_props(props, field_props, {'label': label})
            classes = merge_classes(classes, field_classes)
            styles = build_props(styles, field_styles)
            self.component = 'q-input'
            super().__init__(
                model=model,
                classes=classes,
                styles=styles,
                props=props,
                events=events,
                children=children)


class InputInt(_NumericInput):
    _type = int


class InputFloat(_NumericInput):
    _type = float
