import quasargui
from quasargui.base import Slot
from quasargui.components import Rows
from quasargui.form import Input, Button, Toggle
from quasargui.layout import Layout, Header, Page, Icon

layout = Layout([
    Header(['All form components']),
    Page([Rows([
        Input(label='q-input'),
        Input(label='q-input with slots', props={'bottom-slots': True}, children=[
            Slot('prepend', [Icon('place')]),
            Slot('append', [Icon('close')]),
            Slot('hint', ['Hint slot comes here'])
        ]),
        Toggle(label='q-toggle'),
        Button(label='q-btn', color='primary')
    ])])
])

quasargui.run(layout, debug=True, _render_debug=True)
