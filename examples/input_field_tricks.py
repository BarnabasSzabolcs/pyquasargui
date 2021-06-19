import quasargui
from quasargui import *

isPassword = Model(True)
text_parameter = Model('')

form1 = QForm(styles={'max-width': '30em', 'margin': '0 auto'}, children=[

    QInput(label='simple q-input', model=text_parameter),

    QInput(label='q-input with slots', children=[
        Slot('prepend', [QIcon('place')]),
        Slot('append', [QIcon('close')]),
        Slot('hint', ['Hint slot comes here'])
    ]),

    QInput(
        model=Model("prefilled value"),
        props={
            'clearable': True,
            'clear-icon': 'close',
            'color': 'orange'
        }, children=[
            Slot('label', ['<b>clearable</b> q-input with special colors'])
        ]),

    QInput(
        label='password',
        type=TrueFalse('password', 'text', isPassword),
        children=[
            Slot('append', [QIcon(
                name=TrueFalse('visibility_off', 'visibility', isPassword),
                classes="cursor-pointer",
                events={'click': toggle(isPassword)}
            )])]),

    QInput(label="number input", type='number', props={
        'rules': JSRaw("[value => value>0 || 'Enter a positive number']")
    }),
])

layout = QLayout([
    QHeader(['QInput field tricks']),
    QPage([form1])
])

quasargui.run(layout)
