import quasargui

from quasargui import Model
from quasargui.base import Slot, JSFunction
from quasargui.callbacks import toggle
from quasargui.components import Rows
from quasargui.form import Input, Button, Toggle
from quasargui.layout import Layout, Header, Page, Icon
from quasargui.model import TrueFalse

isPassword = Model(True)

layout = Layout([
    Header(['All form components']),
    Page([Rows([
        Input(label='q-input'),

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

        Toggle(label='q-toggle'),
        Button(label='q-btn', color='primary')
    ])])
])

quasargui.run(layout, debug=True, _render_debug=True)
