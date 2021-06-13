import datetime
from typing import List, Type, Union

from quasargui.base import Component, ComponentWithModel, LabeledComponent, Slot, JSRaw
from quasargui.components import Div, Button, Icon, PopupProxy
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


class FilePicker(LabeledComponent):
    """
    Use rather InputFile
    ref. https://quasar.dev/vue-components/file-picker#qfile-api
    """
    component = 'q-file'


class Toggle(LabeledComponent):
    """
    ref. https://quasar.dev/vue-components/toggle#qtoggle-api
    """
    component = 'q-toggle'
    defaults = {'props': {}}


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


class TimePicker(ComponentWithModel):
    component = 'q-time'


class DatePicker(ComponentWithModel):
    component = 'q-date'


class ColorPicker(ComponentWithModel):
    component = 'q-color'


class InputStr(Input):
    """This is just an alias for the sake of completeness"""


class InputBool(ComponentWithModel):
    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 appearance: str = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: List[Slot] = None):
        self.component = {
            'input': 'q-input',
            'checkbox': 'q-checkbox',
            'toggle': 'q-toggle'
        }[appearance or 'input']
        model = model or Model(False)
        model.set_conversion(bool, bool)
        props = build_props({}, props, {'label': label})
        super().__init__(
            model=model,
            classes=classes,
            styles=styles,
            props=props,
            events=events,
            children=children)


class _NumericInput(ComponentWithModel):
    _type: Type = None
    defaults = {
        'field_classes': 'text-sm',
        'control_props': {}
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
        model.set_conversion(self._type)
        special_props = {
            'min': min,
            'max': max
        }

        if appearance in {'knob', 'slider'}:
            min = 0 if min is None else min
            max = 100 if max is None else max
            component_class = {'knob': Knob, 'slider': Slider}[appearance]

            control_props = build_props({'snap': self._type == int}, props)
            control_props = build_props(self.defaults['control_props'], control_props)
            if self._type == float:
                control_props = build_props({'step': (max-min)/1000}, control_props)
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
            classes = merge_classes(classes or '', field_classes or '')
            styles = build_props(styles or {}, field_styles)
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


class InputFile(LabeledComponent):
    """
    A handily set-up FilePicker.
    ref. https://quasar.dev/vue-components/file-picker#qfile-api
    """
    component = 'q-file'
    defaults = {
        'props': {
            'clearable': True
        }
    }

    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 appearance: str = 'icon',
                 icon: str = 'attachment',
                 icon_left: bool = True,
                 button_caption: str = 'Browse',
                 button_left: bool = False,
                 button_props: PropsType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: List[Slot] = None):
        """
        :param label:
        :param model:
        :param appearance: 'icon' (default) or 'browse'.
        :param icon: icon if appearance == 'icon'
        :param icon_left: the position of the icon if appearance == 'icon'
        :param button_caption: if appearance == 'browse'
        :param button_left: the position of the button if appearance == 'browse'
        :param button_props: the props parameter for the browse button if appearance == 'browse'
        :param classes:
        :param styles:
        :param props:
        :param events:
        :param children:
        """
        children = children or []
        if appearance == 'icon':
            slots = [
                Slot('prepend' if icon_left else 'append', [Icon(icon)])
            ]
            children = slots + children
        elif appearance == 'browse':
            slots = [
                Slot('prepend' if button_left else 'append', [
                    Button(button_caption, props=button_props, events={
                        'click': JSRaw(
                            """
                            (function(e){
                                while(e.tagName !== 'LABEL'){e = e.parentNode}
                                e.getElementsByTagName('input')[0].click()
                            })($event.target)
                            """)
                    })
                ])
            ]
            children = slots + children
        else:
            raise NotImplementedError
        super().__init__(
            label=label,
            model=model,
            classes=classes,
            styles=styles,
            props=props,
            events=events,
            children=children
        )


class _InputWithPicker(ComponentWithModel):
    """
    This component is based on
    https://quasar.dev/vue-components/date#with-qinput

    Create new pickers by changing the configuration of the defaults.
    Pickers go to the popup_slots. (See InputDateTime.)
    """
    component = 'q-input'
    defaults = {
        'props': {},
        'popup_props': {
            'transition-show': 'scale',
            'transition-hide': 'scale',
            'cover': True
        },
        'popup_row_classes': 'row items-center justify-end',
        'picker_props': {},
        'button_props': {
            'label': 'OK',
            'color': 'primary',
            'v-close-popup': None,
            'unelevated': False,
            'flat': True
        },
        'popup_slots': []
    }

    @staticmethod
    def _to_python(s):
        raise NotImplementedError

    @staticmethod
    def _from_python(s):
        return s

    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 props: PropsType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 events: EventsType = None,
                 children: List[Slot] = None):
        props = build_props({}, props, {'label': label})
        model = self._get_model(model)
        children = self._create_popup_slots(model) + (children or [])
        super().__init__(model=model,
                         props=props,
                         classes=classes,
                         styles=styles,
                         events=events,
                         children=children)

    def _create_popup_slots(self, model):
        slots = []
        for position, icon, picker_class in self.defaults['popup_slots']:
            popup = PopupProxy(
                props=self.defaults['popup_props'],
                children=[picker_class(
                    model,
                    props=self.defaults['picker_props'],
                    children=[self._popup_buttons()])
                ])
            slots.append(Slot(position, [
                Icon(name=icon, classes='cursor-pointer', children=[popup])
            ]))
        return slots

    def _get_model(self, model):
        model = model or Model(None)
        model.set_conversion(self._to_python, self._from_python)
        return model

    def _popup_buttons(self):
        return Div(
            classes=self.defaults['popup_row_classes'],
            children=[
                Button(props=self.defaults['button_props'])
            ])

    @classmethod
    def _build_defaults(cls, defaults, custom):
        results = custom.copy()
        for category, settings in defaults.items():
            if category not in results:
                results[category] = settings
            elif '_classes' in category:
                results[category] = merge_classes(settings, results[category])
            elif isinstance(settings, dict):
                results[category] = build_props(settings, results[category])
            else:
                continue
        return results


class InputTime(_InputWithPicker):
    """
    This component is based on
    https://quasar.dev/vue-components/date#example--with-qinput
    """
    defaults = {
        'props': {
            'mask': 'time',
            'rules': ['time']
        },
        'picker_props': {
            'format24h': True
        },
        'popup_slots': [
            ('append', 'access_time', TimePicker),
        ]
    }
    defaults = _InputWithPicker._build_defaults(_InputWithPicker.defaults, defaults)

    @staticmethod
    def _to_python(s):
        return datetime.time.fromisoformat(s)


class InputDate(_InputWithPicker):
    """
    This component is based on
    https://quasar.dev/vue-components/date#example--with-qinput
    """
    defaults = {
        'props': {
            'mask': 'date',
            'rules': ['date']
        },
        'picker_props': {},
        'popup_slots': [
            ('append', 'event', DatePicker),
        ]
    }
    defaults = _InputWithPicker._build_defaults(_InputWithPicker.defaults, defaults)

    @staticmethod
    def _to_python(s):
        return datetime.date.fromisoformat(s.replace('/', '-'))


class InputDateTime(_InputWithPicker):
    """
    This component is based on
    https://quasar.dev/vue-components/date#example--qdate-and-qtime-with-qinput
    """
    defaults = {
        'props': {
            'mask': '####-##-## ##:##',
        },
        'picker_props': {
            'format24h': True,
            'mask': 'YYYY-MM-DD HH:mm',
        },
        'popup_slots': [
            ('prepend', 'event', DatePicker),
            ('append', 'access_time', TimePicker),
        ]
    }
    defaults = _InputWithPicker._build_defaults(_InputWithPicker.defaults, defaults)

    @staticmethod
    def _to_python(s):
        try:
            return datetime.datetime.fromisoformat(s.replace('/', '-'))
        except ValueError:
            return None

    @staticmethod
    def _from_python(dt):
        try:
            return dt.isoformat(sep=' ').rsplit(':', 1)[0]
        except AttributeError:
            return None


class InputColor(_InputWithPicker):
    """
    This component is based on
    https://quasar.dev/vue-components/color-picker#example--input
    """
    defaults = {
        'props': {
            'rules': ['anyColor']
        },
        'picker_props': {},
        'popup_slots': [
            ('append', 'colorize', ColorPicker),
        ]
    }
    defaults = _InputWithPicker._build_defaults(_InputWithPicker.defaults, defaults)

    @staticmethod
    def _to_python(s):
        return s
