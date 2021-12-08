from typing import List

from quasargui.base import Component, ComponentWithModel, LabeledComponent, Model, Slot, Renderable
from quasargui.tools import build_props
from quasargui.typing import PropValueType, ClassesType, StylesType, PropsType, EventsType, ChildrenType


class QInput(ComponentWithModel):
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
            model = model or Model(0)
            model.modifiers.add('number')
        elif props.get('type', '') in {'', 'text'}:
            model = model or Model('')
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


class QSelect(LabeledComponent):
    """
    ref. https://quasar.dev/vue-components/select#qselect-api
    """
    component = 'q-select'


class QFilePicker(LabeledComponent):
    """
    Use rather InputFile
    ref. https://quasar.dev/vue-components/file-picker#qfile-api
    """
    component = 'q-file'


class QForm(Component):
    component = 'q-form'
    defaults = {'classes': 'q-gutter-md'}

    def __init__(self,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 events: EventsType = None,
                 ):
        super().__init__(children=children, classes=classes, styles=styles, events=events)


class QField(LabeledComponent):
    """
    It is a wrapper for custom form fields.
    Basically it provides a label for a field.

    model parameter is for prop 'clearable'
    (if True, and the clear button is pressed, it sets the model to None).
    ref. https://quasar.dev/vue-components/field#qfield-api
    """
    component = 'q-field'
    defaults = {'props': {
        # 'stack-label': True
    }}


class QRadio(LabeledComponent):
    """
    Probably better is to use QOptionGroup (a group of radio's).
    ref. https://quasar.dev/vue-components/radio#qradio-api
    """
    component = 'q-radio'


class QCheckbox(LabeledComponent):
    component = 'q-checkbox'


class QToggle(LabeledComponent):
    """
    ref. https://quasar.dev/vue-components/toggle#qtoggle-api
    """
    component = 'q-toggle'


class QButtonToggle(ComponentWithModel):
    """
    A group of buttons from which one is active at a time.
    ref. https://quasar.dev/vue-components/button-toggle#qbtntoggle-api
    """
    component = 'q-btn-toggle'
    defaults = {'props': {
        'unelevated': True
    }}

    def __init__(self,
                 model: Renderable = None,
                 options: PropValueType = None,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        props = build_props({}, props, {'options': options})
        super().__init__(model=model,
                         children=children,
                         classes=classes,
                         styles=styles,
                         props=props,
                         events=events)


class QOptionGroup(ComponentWithModel):
    """
    prop 'label' does not work in Quasar.
    """
    component = 'q-option-group'
    defaults = {
        'props': {
            'inline': True,
        }}

    # noinspection PyShadowingBuiltins
    def __init__(self,
                 model: Renderable = None,
                 type: PropValueType[str] = None,
                 options: PropValueType = None,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        props = build_props(props or {}, {
            'type': type,
            'options': options,
        })
        if model is not None:
            self._model = model
        elif props.get('type', 'radio') == 'radio':
            self._model = Model('')
        else:
            self._model = Model([])
        super().__init__(model=self._model,
                         children=children,
                         classes=classes,
                         styles=styles,
                         props=props,
                         events=events)


class QKnob(ComponentWithModel):
    """
    ref. https://quasar.dev/vue-components/knob#qknob-api
    """
    component = 'q-knob'
    defaults = {
        'props': {
            'track-color': 'grey-3',
            'color': 'primary',
            'unelevated': True,
            'show-value': True
        }
    }


class QSlider(ComponentWithModel):
    """
    ref. https://quasar.dev/vue-components/slider#qslider-api
    """
    component = 'q-slider'
    defaults = {
        'props': {
            'label': True
        }
    }


class QRange(ComponentWithModel):
    """
    ref. https://quasar.dev/vue-components/range#qrange-api
    """
    component = 'q-range'
    defaults = {
        'props': {
            'label': True
        }
    }


class QTimePicker(ComponentWithModel):
    component = 'q-time'


class QDatePicker(ComponentWithModel):
    component = 'q-date'


class QColorPicker(ComponentWithModel):
    component = 'q-color'
