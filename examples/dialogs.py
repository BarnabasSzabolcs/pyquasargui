from quasargui import *


def show_notification(message):
    layout.notify(message=message, position='top-right', group=False, timeout=1500)


dialog_events = {
    'ok': lambda data: show_notification('OK clicked, data={}'.format(json.dumps(data))),
    'cancel': lambda: show_notification('Cancel clicked'),
    'dismiss': lambda: show_notification('Dialog dismissed'),
}


def show_alert():
    layout.api.plugins.dialog(props={'title': 'Alert', 'message': 'Some message'}, events=dialog_events)


def show_confirm():
    layout.api.plugins.dialog(props={
        'title': 'Confirm',
        'message': 'Would you like to turn on the wifi?',
        'cancel': True,
        'persistent': True
    }, events=dialog_events)


def show_prompt():
    layout.api.plugins.dialog(props={
        'title': 'Prompt',
        'message': 'What is your name?',
        'prompt': {'model': '', 'type': 'text'},
        'cancel': True,
        'persistent': True
    }, events=dialog_events)


def show_options():
    layout.api.plugins.dialog(props={
        'title': 'Options',
        'message': 'Choose an option',
        'options': {
            'model': 'opt1',
            'type': 'radio',
            'items': [
                {'label': 'Option 1', 'value': 'opt1', 'color': 'secondary'},
                {'label': 'Option 2', 'value': 'opt2'},
                {'label': 'Option 3', 'value': 'opt3'}
            ]
        },
        'cancel': True,
        'persistent': True
    }, events=dialog_events)


def show_bottom_sheet(grid: bool):
    layout.api.plugins.bottom_sheet(props={
        'message': 'Bottom Sheet message',
        'grid': grid,
        'actions': [
            {'label': 'Drive', 'id': 'drive', 'img': 'https://cdn.quasar.dev/img/logo_drive_128px.png'},
            {'label': 'Keep', 'id': 'keep', 'img': 'https://cdn.quasar.dev/img/logo_keep_128px.png'},
            {'label': 'Google Hangouts', 'id': 'calendar', 'img': 'https://cdn.quasar.dev/img/logo_hangouts_128px.png'},
            {},
            {'label': 'Share', 'icon': 'share', 'id': 'share'},
            {'label': 'Upload', 'icon': 'cloud_upload', 'color': 'primary', 'id': 'upload'},
            {},
            {'label': 'John', 'avatar': 'https://cdn.quasar.dev/img/boy-avatar.png', 'id': 'john'}
        ]

    }, events=dialog_events)


dark_mode = Model(False)
dark_mode.add_callback(
    lambda: layout.api.plugins.dark(dark_mode.value)
)

layout = QLayout([
    QHeader([QToolbar([
        QToolbarTitle([
            QIcon('announcement', 'lg', classes='q-mx-md'),
            'Dialogs'
        ]),
        QSpace(),
        QButton(
            label=Computed(lambda dark: 'light mode' if dark else 'dark mode', dark_mode),
            icon=Computed(lambda dark: 'light_mode' if dark else 'dark_mode', dark_mode),
            props={'stretch': True},
            events={'click': toggle(dark_mode)}
        )
    ])]),
    QPage([Rows(classes='q-py-xl', children=[

        QButton('show an alert', events={'click': show_alert}),
        QButton('show a confirmation', events={'click': show_confirm}),
        QButton('show a prompt', events={'click': show_prompt}),
        QButton('show options', events={'click': show_options}),
        QButton('show a grid menu', events={'click': lambda: show_bottom_sheet(grid=True)}),
        QButton('show a list menu', events={'click': lambda: show_bottom_sheet(grid=False)}),

        Div(classes='q-my-xl', children=[
            'See even more examples at ',
            Link('Quasar dialog documentation',
                 'https://quasar.dev/quasar-plugins/dialog#predefined')])
    ])])
])

run(layout, title='Dialogs demonstration', debug=True)
