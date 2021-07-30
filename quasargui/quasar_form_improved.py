"""
Improved controls for data input.
The logic is that you choose your datatype
and a corresponding appearance that fits.

Everything is set up for convenience.
"""

import datetime
from typing import List, Type, Union

from quasargui.base import Component, ComponentWithModel, LabeledComponent, Slot, JSRaw
from quasargui.components import Div
from quasargui.model import Model, Renderable, Computed, Reactive
from quasargui.quasar_components import QButton, QEditor, QIcon, QPopupProxy
from quasargui.quasar_form import (
    QInput, QSelect, QField, QButtonToggle, QOptionGroup, QKnob, QSlider,
    QTimePicker, QDatePicker, QColorPicker)
from quasargui.tools import build_props, merge_classes
from quasargui.typing import ClassesType, StylesType, PropsType, EventsType
from quasargui.vue_tags_input import VueTagsInput


class InputStr(QInput):
    """This is just an alias for the sake of completeness"""


class InputText(Component):
    """
    NOTE: This component does not work.
    """
    defaults = {
        'label_classes': 'q-mt-sm'
    }

    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 appearance: str = 'editor',
                 classes: ClassesType = None,
                 label_classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: List[Slot] = None):
        """
        :param label:
        :param model:
        :param appearance: 'editor' or 'textarea'
        :param classes:
        :param styles:
        :param props:
        :param events:
        :param children:
        """
        model = model or Model('')
        if appearance == 'editor':
            raise NotImplementedError('Cannot use appearance == "editor" '
                                      'at the moment since it is not editable for some reason'
                                      'and we couldn\'t fix it.')
            self.component = 'div'
            children = [
                label,
                QEditor(model=model, classes=classes, styles=styles, props=props, events=events, children=children)
            ]
            label_classes = merge_classes(self.defaults['label_classes'], label_classes)
            super().__init__(classes=label_classes, children=children)
        else:
            self.component = 'q-input'
            props = build_props({'type': 'textarea'}, props, {
                'label': label,
                'v-model': model
            })
            super().__init__(
                classes=classes,
                styles=styles,
                props=props,
                events=events,
                children=children)


class InputBool(LabeledComponent):
    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 appearance: str = 'checkbox',
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: List[Slot] = None):
        self.component = {
            'checkbox': 'q-checkbox',
            'toggle': 'q-toggle'
        }[appearance]
        model = model or Model(False)
        model.set_conversion(bool, bool)
        super().__init__(
            label=label,
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
            component_class = {'knob': QKnob, 'slider': QSlider}[appearance]

            control_props = build_props({'snap': self._type == int}, props)
            control_props = build_props(self.defaults['control_props'], control_props)
            if self._type == float:
                control_props = build_props({'step': (max - min) / 1000}, control_props)
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


class InputChoice(LabeledComponent):
    component = 'div'
    defaults = {
        'item_props': {
            'clearable': True  # this prop does not work with radio, with everything else it does.
        }
    }

    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 choices: Union[Renderable, list] = None,
                 multiple: bool = None,
                 appearance: str = 'auto',
                 item_props: PropsType = None,
                 label_props: PropsType = None,
                 props: PropsType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 events: EventsType = None):
        """
        :param label:
        :param model:
            the value of the model depends on the choices parameter (and the item_props).
            List[str] choice format yields the displayed label as model value,
            List[dict] format yields the value of 'value' field as value, if dict has only 'label' and 'value' fields.
            Otherwise List[dict] format yields the whole dict of the selected item.
            This behavior can be overridden with item_props
            that is sent to QSelect ('select'), QOptionGroup ('radio') or QButtonToggle ('buttons') as props parameter.
        :param choices: format is ['choice 1', 'choice 2', ...] or [{'label':'Choice 1', 'value': 1}, ...].
        :param appearance:
            if multiple=False: 'auto', 'radio', 'buttons' or 'select'.
            'auto' means 'radio' for small lists, 'select' for large lists.
            if multiple=True: 'auto', 'checkboxes', 'toggles', 'select' or 'tags'
            'auto' means 'checkboxes' for small lists, 'select' for large lists, 'tags' if choices is None.
        :param item_props: The props for the items. (also if appearance=='select', props for the QSelect)
        :param classes:
        :param styles:
        :param label_props:
        :param events:
        """

        def is_lvc(choices_):
            """
            is_label_value_choice
            """
            # noinspection PyBroadException
            try:
                return set(choices_[0].keys()) == {'label', 'value'}
            except Exception:
                return False

        single_only_appearances = {'input', 'radio', 'buttons'}
        multiple_only_appearances = {'checkboxes', 'toggles', 'tags'}
        props = props or {}

        if multiple is None:
            multiple = appearance in multiple_only_appearances

        model = model or Model([] if multiple else '')
        self.dependents = [model]

        allowed_appearances = {'auto', 'radio', 'checkboxes', 'toggles', 'buttons', 'select', 'tags'}
        if appearance not in allowed_appearances:
            raise AssertionError('Wrong appearance {}. Must be one of {}'.format(appearance, allowed_appearances))
        if appearance in single_only_appearances and multiple:
            raise AssertionError('appearance=={} can be only used if multiple==False'.format(appearance))
        elif appearance in multiple_only_appearances and not multiple:
            raise AssertionError('appearance=={} can be only used if multiple==True'.format(appearance))

        if appearance == 'auto':
            # auto is for providing the user a reasonable default.
            if isinstance(choices, list):
                n_choices = len(choices)
            elif isinstance(choices, Reactive):
                n_choices = len(choices.value)
            else:
                n_choices = 0
            if multiple:
                appearance = (
                    'tags' if n_choices == 0 else
                    'checkboxes' if n_choices <= 10 else
                    'select'
                )
            else:
                appearance = 'radio' if 0 < n_choices <= 5 else \
                             'input' if n_choices == 0 else \
                             'select'

        if appearance == 'input':
            self.component = 'q-input'
            children = []
        elif appearance in {'radio', 'buttons', 'checkboxes', 'toggles'}:
            if (isinstance(choices, list) and len(choices)
                    and isinstance(choices[0], str)):
                choices = [{'label': choice, 'value': choice} for choice in choices]
            default_item_props = build_props(
                self.defaults['item_props'],
                {'type': 'radio'} if appearance == 'radio' else
                {'type': 'checkbox'} if appearance == 'checkboxes' else
                {'type': 'toggle'} if appearance == 'toggles' else
                {})
            item_props = build_props(
                default_item_props,
                item_props)
            children = [
                Div([label], props=label_props),
            ]
            if appearance in {'radio', 'checkboxes', 'toggles'}:
                del item_props['clearable']
                type_ = {
                    'radio': 'radio',
                    'checkboxes': 'checkbox',
                    'toggles': 'toggle',
                }[appearance]
                children += [QOptionGroup(model=model, type=type_, options=choices, props=item_props)]
            elif appearance == 'buttons':
                children += [QButtonToggle(model=model, options=choices, props=item_props)]
        elif appearance == 'select':
            if isinstance(choices, Reactive):
                is_label_value_choice = Computed(is_lvc, choices)
            else:
                is_label_value_choice = is_lvc(choices)
            default_props = {
                'emit-value': is_label_value_choice,
                'map-options': is_label_value_choice
            }
            default_props = build_props(default_props, self.defaults['item_props'])
            item_props = build_props(
                default_props,
                item_props,
                {
                    'options': choices,
                    'multiple': multiple,
                    'use-chips': multiple
                }
            )
            children = [QSelect(label=label, model=model, props=item_props)]
        elif appearance == 'tags':
            label_props = build_props({
                'hide-bottom-space': True,
            }, label_props)
            item_props = build_props({
                'placeholder': props.get('placeholder', ''),
                'add-on-key': [13, ','],
                # 'separators': [',']
            }, item_props)
            children = [
                QField(label=label, model=model, props=label_props, children=[
                    Slot('control', [
                        VueTagsInput(model, props=item_props)
                    ])
                ]),
            ]
        else:
            raise NotImplementedError('appearance=={} is not implemented.'.format(appearance))
        super().__init__(
            label=label,
            model=model,
            classes=classes,
            styles=styles,
            props=props,
            events=events,
            children=children
        )


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
                Slot('prepend' if icon_left else 'append', [QIcon(icon)])
            ]
            children = slots + children
        elif appearance == 'browse':
            slots = [
                Slot('prepend' if button_left else 'append', [
                    QButton(button_caption, props=button_props, events={
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
            popup = QPopupProxy(
                props=self.defaults['popup_props'],
                children=[picker_class(
                    model,
                    props=self.defaults['picker_props'],
                    children=[self._popup_buttons()])
                ])
            slots.append(Slot(position, [
                QIcon(name=icon, classes='cursor-pointer', children=[popup])
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
                QButton(props=self.defaults['button_props'])
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
            ('append', 'access_time', QTimePicker),
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
            ('append', 'event', QDatePicker),
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
            ('prepend', 'event', QDatePicker),
            ('append', 'access_time', QTimePicker),
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
            ('append', 'colorize', QColorPicker),
        ]
    }
    defaults = _InputWithPicker._build_defaults(_InputWithPicker.defaults, defaults)

    @staticmethod
    def _to_python(s):
        return s
