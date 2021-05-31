import quasargui
from quasargui import *

isPassword = Model(True)
text_parameter = Model('')

form1 = Form(styles={'max-width': '30em', 'margin': '0 auto'}, children=[

    Input(label='simple q-input', model=text_parameter),

    Input(label='q-input with slots', children=[
        Slot('prepend', [Icon('place')]),
        Slot('append', [Icon('close')]),
        Slot('hint', ['Hint slot comes here'])
    ]),

    Input(
        model=Model("prefilled value"),
        props={
            'clearable': True,
            'clear-icon': 'close',
            'color': 'orange'
        }, children=[
            Slot('label', ['<b>clearable</b> q-input with special colors'])
        ]),

    Input(
        label='password',
        type=TrueFalse('password', 'text', isPassword),
        children=[
            Slot('append', [Icon(
                name=TrueFalse('visibility_off', 'visibility', isPassword),
                classes="cursor-pointer",
                events={'click': toggle(isPassword)}
            )])]),

    Input(label="number input", type='number', props={
        'rules': JSFunction("[value => value>0 || 'Enter a positive number']")
    }),
])

layout = Layout([
    Header(['Input field tricks']),
    Page([form1])
])

quasargui.run(layout)
