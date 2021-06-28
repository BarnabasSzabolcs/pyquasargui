from quasargui import Model, QLayout, QHeader, QPage, QToolbar, QSpace, QButton, QInput, Rows, TrueFalse, toggle
from quasargui.main import run


title_model = Model('Your title goes here')
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


def toggle_fullscreen():
    layout.api.toggle_fullscreen()
    is_fullscreen.value = not is_fullscreen.value


layout = QLayout([
    QHeader([QToolbar([
        QSpace(),
        QButton(icon='minimize',
                props={'stretch': True},
                events={'click': lambda: layout.api.minimize_window()}),
        QButton(icon=TrueFalse('fullscreen_exit', 'fullscreen', is_fullscreen),
                props={'stretch': True},
                events={'click': toggle_fullscreen}),
        QButton(icon='close',
                props={'stretch': True},
                events={'click': lambda: layout.api.close_window()}),
    ])]),
    QPage([
        Rows([
            QInput('Window title', title_model),
            QInput('Resize window width', width, type='number'),
            QInput('Resize window height', height, type='number'),
            QButton(
                'Show file dialog',
                events={
                    'click': lambda: layout.notify('You chose: {}'.format(
                        layout.api.show_open_dialog()))
                }),
            QButton(
                'Show folder dialog',
                events={
                    'click': lambda: layout.notify('You chose: {}'.format(
                        layout.api.show_folder_dialog()))
                }),
            QButton(
                'Show save dialog',
                events={
                    'click': lambda: layout.notify('You chose: {}'.format(
                        layout.api.show_save_dialog()))
                }),
        ])
    ])
])

run(layout, size=(400, 500))
