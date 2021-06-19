import json

from quasargui import *


def show_notification(message):
    layout.api.show_notification(message=message, position='top-right', group=False, timeout=1500)


dialog_events = {
    'ok': lambda data: show_notification('OK clicked, data={}'.format(json.dumps(data))),
    'cancel': lambda: show_notification('Cancel clicked'),
    'dismiss': lambda: show_notification('Dialog dismissed'),
}


def show_alert():
    layout.api.show_dialog(props={'title': 'Alert', 'message': 'Some message'}, events=dialog_events)


def show_confirm():
    layout.api.show_dialog(props={
        'title': 'Confirm',
        'message': 'Would you like to turn on the wifi?',
        'cancel': True,
        'persistent': True
    }, events=dialog_events)


def show_prompt():
    layout.api.show_dialog(props={
        'title': 'Prompt',
        'message': 'What is your name?',
        'prompt': {'model': '', 'type': 'text'},
        'cancel': True,
        'persistent': True
    }, events=dialog_events)


def show_options():
    layout.api.show_dialog(props={
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


layout = QLayout([QPage([Rows(classes='q-pa-lg', children=[
    QButton('show an alert', events={'click': show_alert}),
    QButton('show a confirmation', events={'click': show_confirm}),
    QButton('show a prompt', events={'click': show_prompt}),
    QButton('show options', events={'click': show_options}),
    Div(classes='q-ma-lg', children=[
        'See even more examples at ',
        Link('Quasar dialog documentation',
             'https://quasar.dev/quasar-plugins/dialog#predefined')])
])])])

run(layout, debug=True)
