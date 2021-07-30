from quasargui import *

props = {
    'dense': True
}

QButton.defaults['props'] = {
    'dense': True,
    'unelevated': True
}
Columns.defaults['classes'] = ''
Rows.defaults['classes'] = ''


layout = QLayout(children=[
    QPage([
        QBar(props={'dense': True}, classes='q-pr-xs', children=[
            QSpace(),
            QButton(icon='minimize',
                    props=props,
                    events={'click': lambda: layout.api.minimize_window()}),
            QButton(icon='close',
                    props=props,
                    events={'click': lambda: layout.api.close_window()}),
        ]),
        Rows([
            Columns([QButton(icon='language'), QButton(icon='favorite')]),
            Columns([QButton(icon='send'), QButton(icon='help')]),
        ])
    ])
])

run(layout, frameless=True, size=(64, 100), resizable=False)
