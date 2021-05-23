"""
This example showcases
 - form submission and error checking,
 - replacing the window layout,
 - creating rows and columns.
"""

import quasargui
from quasargui import set_main_component, Model
from quasargui.callbacks import bind
from quasargui.components import Div, Rows, Columns, Input, Button


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
    Button(
        label=str(i),
        color=colors[i],
        props={'padding': 'xs xs'},
        styles={'min-width': '3em'},
        events={'click': bind(set_color, colors[i])}
    )
    for i in range(MAX_BUTTONS)
]


result_layout = Rows(classes='q-ma-lg', children=[
    "(placeholder for the buttons)",
    Columns(classes='q-gutter-x-xs q-my-md', children=[
        Button(
            label='Back',
            color='grey-7',
            events={'click': lambda: set_main_component(form_layout)}),
        Button(
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
        Input(
            model=n_buttons,
            styles={'min-width': "30em"},
            props={'label': 'Enter a number between 1 and 100'}),
        Div(
            props={'v-if': n_buttons},
            classes="q-ml-sm",
            children=["You have entered: ", n_buttons]),
        Button(
            label='ok',
            props={'color': 'primary'},
            events={'click': show_buttons_table})
    ])

quasargui.run(form_layout)
