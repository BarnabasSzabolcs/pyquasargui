import quasargui
from quasargui import *


form1 = Form(styles={'max-width': '30em', 'margin': '0 auto'}, children=[
    Heading(5, 'Inputs by value type'),
    InputStr('str input'),  # Input
    # InputDate(),  # Input + popup Date
    # InputTime(),  # Input + popup Time
    # InputDateTime(),  # Input + popup date + popup time
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
