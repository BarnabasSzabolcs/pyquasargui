from random import randint
from time import sleep

from quasargui import Model, QLayout, QHeader, QPage, QToolbar, QSpace, QButton, QInput, Rows, TrueFalse
from quasargui.main import create_window, run


def create_new_window():
    layout = create_layout('New window')
    create_window(layout, position=(randint(1, 100), randint(1, 100)), size=(400, 500))
    sleep(0.5)
    layout.api.plugins.notify(message='A brand new window!', type='positive')


def close_window(layout):
    layout.api.close_window()
    print('The window is closed but the app still runs')


def toggle_fullscreen(layout, model):
    model.value = not model.value
    layout.api.toggle_fullscreen()


def save_dialog(api):
    result = api.show_save_dialog()
    api.plugins.notify(message='Result: {}'.format(result))


def open_dialog(api):
    result = api.show_open_dialog()
    api.plugins.notify(message='Result: {}'.format(result))


def folder_dialog(api):
    result = api.show_folder_dialog()
    api.plugins.notify(message='Result: {}'.format(result))


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
    height = Model(500)
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
                QInput('Window title', title_model),
                QInput('Resize window width', width, type='number'),
                QInput('Resize window height', height, type='number'),
                QButton('Create new window', events={'click': create_new_window}),
                QButton('Open file dialog', events={'click': lambda: open_dialog(layout.api)}),
                QButton('Open folder dialog', events={'click': lambda: folder_dialog(layout.api)}),
                QButton('Open save dialog', events={'click': lambda: save_dialog(layout.api)}),
            ])
        ])
    ])
    return layout


main_layout = create_layout('Main window')
run(main_layout, size=(400, 500))
