"""
From this example you can learn how to set a menu,
and how to declare it dynamically (eg. for internationalization).

At the moment, the menu only works for Mac/Cocoa render.
"""

from quasargui import *
from quasargui.tools import static_vars

menu = [
    {'title': 'Top Action', 'action': lambda: layout.notify("Top Action"), 'key': 't'},
    {'title': 'Custom menu 1', 'children': [
        {'title': 'Action 1', 'action': lambda: layout.notify("Hello 1"), 'key': 'b'},
        {'title': 'Action 2', 'action': lambda: layout.notify("Hello 2"), 'key': 'd'},
        None,  # separator
        {'title': 'Submenu', 'children': [
            {'title': 'Action 3', 'action': lambda: layout.notify("Hello 3")},
            {'title': 'Submenu 2', 'children': [
                {'title': 'Submenu goes forever:)', 'children': [
                    {'title': 'Action 5', 'action': lambda: layout.notify("Hello 5")}
                ]},
                {'title': 'Action 4', 'action': lambda: layout.notify("Hello 4")}
            ]},
        ]},
    ]},
]


@static_vars(counter=0)
def switch_menu():
    new_menu = [{'title': 'Alternative action', 'action': lambda: layout.notify("Alternative action")}]
    switch_menu.counter += 1
    if switch_menu.counter % 2 == 1:
        layout.api.set_menu(new_menu)
    else:
        layout.api.set_menu(menu)


@static_vars(spare_menu=None)
def hide_menu_if_not(platform):
    layout.api.set_menu({platform: menu, 'default': []})


props = {'clickable': True}

layout = Rows(
    classes='q-ma-lg',
    children=[
        Heading(5, 'Click on a menu'),
        QList(props={'bordered': True}, classes='rounded-borders', children=[
            QItem([QItemSection(['Replace menu with alternative menu'])], props=props, events={'click': switch_menu}),
            QItem([QItemSection(['No menu if not Mac'])], props=props, events={'click': lambda: hide_menu_if_not('mac')}),
            QItem([QItemSection(['No menu if not Windows'])], props=props, events={'click': lambda: hide_menu_if_not('windows')})
        ])
    ])

run(layout, menu=menu)
