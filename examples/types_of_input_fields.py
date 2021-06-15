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

form1 = Form(styles={'max-width': '20em', 'margin': '0 auto'}, children=[
    Heading(5, 'Inputs by value type'),
    InputStr('str input'),  # Input
    InputStr('str input - type textarea', type='textarea'),

    InputInt('int input slider [-3, 3]', appearance='slider', min=-3, max=3),  # input, knob or slider
    InputInt('int input [-3, 3]', min=-3, max=3),  # input, knob or slider

    InputFloat('float input [0.0, 100.0]', appearance='knob'),  # input, knob or slider
    InputFloat('float input [-3.0, 3.0]', appearance='slider', min=-3.0, max=3.0),  # input, knob or slider

    InputBool('bool input', appearance='toggle'),  # toggle or checkbox
    InputBool('bool input', appearance='checkbox'),  # toggle or checkbox

    InputChoice('input choice', choices=['a', 'b', 'c'], appearance='radio'),
    InputChoice('input choice', choices=['a', 'b', 'c'], appearance='buttons'),
    InputChoice('input choice', choices=['a', 'b', 'c'], appearance='select'),
    InputChoice('input choice - user friendly', model=choice, choices=choices, appearance='radio'),
    InputChoice('input choice - user friendly', model=choice, choices=choices, appearance='buttons'),
    InputChoice('input choice - user friendly', model=choice, choices=choices, appearance='select'),

    # InputList(appearance='tags'),
    # InputList(appearance='select'),
    # InputList(appearance='checkbox'),  # checkbox (OptionGroup)
    # InputList(appearance='toggle'),  # toggle (OptionGroup)

    InputColor('color input'),  # Input + popup Color
    InputDate('date input', my_date),  # Input + popup Date
    InputTime('time input', my_time),  # Input + popup Time
    InputDateTime('datetime input', my_datetime),  # Input + popup date + popup time
    InputFile('file input', appearance='icon'),  # File with attachment icon
    InputFile('file input', appearance='browse'),  # File with browse button

    Heading(5, 'Inputs by Quasar components'),
    Input('vanilla input'),
    Input('textarea input', type='textarea'),
    Input('oldschool number input', type='number'),
    FilePicker('vanilla file picker'),
    # Select(), TagsInput(), Radio(), ButtonToggle(),
    Slider(model=Model()),
    # Range(Model()),  # OptionGroup(type="checkbox"), # radio, toggle
    Toggle(),  # Checkbox(),
    TimePicker(Model()),
    DatePicker(Model()),
])
layout = Layout([
    Header([Icon('table_view', 'lg', classes='q-mx-md'), 'Fields for different types of data']),
    Page([form1])
])

quasargui.run(layout, debug=True, _render_debug=True)
