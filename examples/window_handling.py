from random import randint
from time import sleep

from quasargui import *
from quasargui.main import create_window


def create_new_window():
    layout = create_layout('New window')
    create_window(layout, position=(randint(1, 100), randint(1, 100)))
    sleep(0.5)
    layout.api.plugins.notify(message='A brand new window!', type='positive')


def close_window(layout):
    layout.api.close_window()
    print('The window is closed but the app still runs')


def toggle_fullscreen(layout, model):
    model.value = not model.value
    layout.api.toggle_fullscreen()


def create_layout(title):
    title_model = Model(title)
    title_model.add_callback(
        lambda: title_model.api.set_window_title(title_model.value),
        immediate=True
    )
    is_fullscreen = Model(False)

    layout = QLayout([
        QHeader([QToolbar([
            QSpace(),
            QButton(icon='minimize',
                    props={'stretch': True},
                    events={'click': lambda: layout.api.minimize_window()}),
            QButton(icon=TrueFalse('fullscreen_exit', 'fullscreen', is_fullscreen),
                    props={'stretch': True},
                    events={'click': lambda: toggle_fullscreen(layout, is_fullscreen)}),
            QButton(icon='close',
                    props={'stretch': True},
                    events={'click': lambda: close_window(layout)}),
        ])]),
        QPage([
            Rows([
                QInput('Window title', title_model),
                QButton('Create new window', events={'click': create_new_window})
            ])
        ])
    ])
    return layout


layout = create_layout('Main window')
run(layout)
