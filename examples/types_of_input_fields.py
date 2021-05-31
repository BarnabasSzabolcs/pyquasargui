from datetime import datetime as dt

import quasargui
from quasargui import *

my_date = Model(None)
my_date.add_callback(lambda: my_date.api.show_notification({
    'message': f'Selected date: {my_date.value} ({type(my_date.value)}).',
}))
my_time = Model(None)
my_time.add_callback(lambda: my_time.api.show_notification({
    'message': f'Selected time: {my_time.value} ({type(my_time.value)}).',
}))
my_datetime = DateTimeModel(dt.now())
my_datetime.add_callback(lambda: my_datetime.api.show_notification({
    'message': f'Selected date and time: {my_datetime.value} ({type(my_datetime.value)}).',
}))
form1 = Form(styles={'max-width': '30em', 'margin': '0 auto'}, children=[
    Heading(5, 'Inputs by value type'),
    InputStr('str input'),  # Input
    InputDate('date input', my_date),  # Input + popup Date
    InputTime('time input', my_time),  # Input + popup Time
    InputDateTime('datetime input', my_datetime),  # Input + popup date + popup time
    # InputFile(appearance='browse'),  # File with attachment icon or browse button
    InputInt('int input', appearance='slider', min=-3, max=3),  # input, knob, slider
    InputFloat('float input', appearance='knob'),  # input, knob, slider
    # InputList(),  # tags, select multiple
    # InputBool(appearance='button'),  # toggle or checkbox
    # InputColor(),  # Input + popup Color

    Input(),
    # Date(),
    # Time(),
    # File(),
    Input(type='number'),
    Input(type='number'),
    # Select(), TagsInput(),
    # Toggle(), Checkbox(), ButtonToggle(),
])
layout = Layout([
    Header(['Fields for different types of data']),
    Page([form1])
])

quasargui.run(layout, debug=True, _render_debug=True)
