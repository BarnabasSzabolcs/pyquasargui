"""
This example showcases
 - form submission and error checking,
 - replacing the window layout,
 - creating rows and columns.
"""

import quasargui
from quasargui import *


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


MAX_BUTTONS = 100
colors = [Model('primary') for i in range(MAX_BUTTONS)]


def set_color(color):
    color.value = 'positive' if color.value == 'primary' else 'primary'


def reset_colors():
    for color in colors:
        color.value = 'primary'


buttons = [
    QButton(
        label=str(i),
        color=colors[i],
        props={'padding': 'xs xs'},
        styles={'min-width': '3em'},
        events={'click': call(set_color, colors[i])}
    )
    for i in range(MAX_BUTTONS)
]


result_layout = Rows(classes='q-ma-lg', children=[
    "(placeholder for the buttons)",
    Columns(classes='q-gutter-x-xs q-my-md', children=[
        QButton(
            label='Back',
            color='grey-7',
            events={'click': lambda: set_main_component(form_layout)}),
        QButton(
            label='Reset',
            color='grey-7',
            events={'click': lambda: reset_colors()})
    ])
])


def show_buttons_table():
    try:
        i = int(n_buttons.value)
    except ValueError:
        form_layout.notify("Please enter digits", type='negative', icon='warning')
        n_buttons.value = ''
        return
    if i < 1 or i > 100:
        form_layout.notify("Number not in range", type='negative', icon='warning')
        n_buttons.value = ''
        return
    result_layout.set_children([
        Columns([Rows(rows) for rows in chunks(buttons[:i], 10)]),
        *result_layout.children[1:]
    ])
    set_main_component(result_layout)


n_buttons = Model('')


form_layout = Rows(
    classes='q-ma-lg q-gutter-md',
    children=[
        '<h5>Dynamic components</h5>',
        QInput(
            label='Enter a number between 1 and 100',
            model=n_buttons,
            styles={'min-width': "30em"}),
        v_if(
            n_buttons,
            Div(
                classes="q-ml-sm",
                children=["You have entered: ", n_buttons])
        ),
        QButton(
            label='ok',
            props={'color': 'primary'},
            events={'click': show_buttons_table})
    ])

quasargui.run(form_layout)
