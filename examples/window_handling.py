from random import randint
from time import sleep

from quasargui import *
from quasargui.main import create_window


def create_new_window():
    layout = create_layout('New window')
    create_window(layout, position=(randint(1, 100), randint(1, 100)), size=(400, 400))
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
    width = Model(400)
    width.add_callback(
        lambda: width.api.resize_window((width.value, None)) if 300 <= width.value <= 1000 else None,
        immediate=True
    )
    height = Model(400)
    height.add_callback(
        lambda: height.api.resize_window((None, height.value)) if 300 <= height.value <= 1000 else None,
        immediate=True
    )

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
                InputStr('Window title', title_model),
                QButton('Create new window', events={'click': create_new_window}),
                QInput('Resize window width', width, type='number'),
                QInput('Resize window height', height, type='number'),
            ])
        ])
    ])
    return layout


layout = create_layout('Main window')
run(layout, size=(400, 400))
