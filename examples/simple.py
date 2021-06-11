import quasargui
from quasargui import *


def run_program():
    layout.notify('Hello, {name}!'.format(
        name=input_name.value
    ))


input_name = Input(
    # # uncomment these lines if you want to display notification message on change:
    # value='',
    # events={'change': run_program}
)
btn_submit = Button(
    label='Submit',
    classes='text-primary',
    props={'unelevated': True, 'size': 'lg'},
    events={'click': run_program})

layout = Div(
    styles={
        'max-width': '30em',
        'margin-left': 'auto',
        'margin-right': 'auto',
    },
    classes='q-mt-xl text-center',
    children=[
        "What's your name?",
        input_name,
        btn_submit])


quasargui.run(layout)
