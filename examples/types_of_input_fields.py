from datetime import datetime as dt

import quasargui
from quasargui import *

my_date = Model(None)
my_date.add_callback(lambda: my_date.api.show_notification(
    message='Selected date: {} ({}).'.format(my_date.value, type(my_date.value))
))
my_time = Model(None)
my_time.add_callback(lambda: my_time.api.show_notification(
    message='Selected time: {} ({}).'.format(my_time.value, type(my_time.value))
))
my_datetime = DateTimeModel(dt.now())
my_datetime.add_callback(lambda: my_datetime.api.show_notification(
    message='Selected date and time: {} ({}).'.format(my_datetime.value, type(my_datetime.value))
))

choices = [
    {'label': 'Alpha (a)', 'value': 'a'},
    {'label': 'Bravo (b)', 'value': 'b'},
    {'label': 'Charlie (c)', 'value': 'c'}
]
choice = Model()
choice.add_callback(lambda: layout.notify('Selected: {}'.format(choice.value)))

form1 = Form(styles={'max-width': '30em', 'margin': '0 auto'}, children=[
    QList(props={'bordered': True}, classes='rounded-borders', children=[
        ExpansionItem(
            'Inputs by type of input value',
            classes='q-pa-md',
            props={
                'caption': 'These controls are set up for least effort and flexibility'
            },
            children=[Card([CardSection([
                # Heading(5, 'Inputs by value type'),
                InputStr('str input'),  # Input
                InputStr('str input - type textarea', type='textarea'),

                InputInt('int input slider [-3, 3]', appearance='slider', min=-3, max=3),  # input, knob or slider
                InputInt('int input [-3, 3]', min=-3, max=3),  # input, knob or slider

                InputFloat('float input [0.0, 100.0]', appearance='knob'),  # input, knob or slider
                InputFloat('float input [-3.0, 3.0]', appearance='slider', min=-3.0, max=3.0),  # input, knob or slider

                InputBool('bool input'),
                InputBool('bool input', appearance='toggle'),

                InputChoice('input choice', choices=['a', 'b', 'c']),
                InputChoice('input choice', choices=['a', 'b', 'c'], appearance='buttons'),
                InputChoice('input choice', choices=['a', 'b', 'c', 'd', 'e', 'f']),
                InputChoice('input choice - custom label', model=choice, choices=choices, appearance='radio'),
                InputChoice('input choice - custom label', model=choice, choices=choices, appearance='buttons'),
                InputChoice('input choice - custom label', model=choice, choices=choices, appearance='select'),

                InputChoice('input choice - checkboxes', appearance='checkboxes', choices=choices),
                InputChoice('input choice - toggles', appearance='toggles', choices=choices),
                InputChoice('input choice - select multiple', appearance='select', multiple=True, choices=choices),
                InputChoice('input choice - tags', appearance='tags'),

                # InputObject(),  # this is going to be a textarea, the idea is to support assigning arbitrary data.
                # InputCode(),  # since python can execute code, why not enable the user to do it?

                InputColor('color input'),  # Input + popup Color
                InputDate('date input', my_date),  # Input + popup Date
                InputTime('time input', my_time),  # Input + popup Time
                InputDateTime('datetime input', my_datetime),  # Input + popup date + popup time
                InputFile('file input', appearance='icon'),  # File with attachment icon
                InputFile('file input', appearance='browse'),  # File with browse button
            ])])]
        ),
        ExpansionItem(
            'Original Quasar Inputs',
            classes='q-pa-md',
            props={
                'caption': 'Use this controls if you want to build some custom logic'
            },
            children=[Card([CardSection([
                # Heading(5, 'Inputs by Quasar components'),
                Input('vanilla input'),
                Input('textarea input', type='textarea'),
                Input('oldschool number input', type='number'),
                FilePicker('vanilla file picker'),
                Select('select'),
                Checkbox('checkbox'),
                Radio('radio'),
                Toggle('toggle'),
                VueTagsInput(),
                ButtonToggle(props={'options': choices}),
                Slider(model=Model()),
                Range(Model()),
                OptionGroup(type="checkbox", options=choices),
                OptionGroup(type="radio", options=choices),
                OptionGroup(type="toggle", options=choices),
                TimePicker(Model()),
                DatePicker(Model()),
            ])])]
        )
    ]),
])
layout = Layout([
    Header([Icon('table_view', 'lg', classes='q-mx-md'), 'Fields for different types of data']),
    Page([form1])
])

quasargui.run(layout)
