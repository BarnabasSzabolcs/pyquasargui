"""
From this example you can learn how to set a menu,
and how to declare it dynamically (eg. for internationalization).

At the moment, the menu only works for Mac/Cocoa render.
"""

from quasargui import *


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


def switch_menu():
    new_menu = [
        {'title': 'Alternative action', 'action': lambda: layout.notify("Alternative action")},
    ]
    if layout.api.menu[0]['title'] != new_menu[0]['title']:
        layout.api.set_menu(new_menu)
    else:
        layout.api.set_menu(menu)


layout = Rows(
    classes='q-ma-lg',
    children=[
        'Click on a menu',
        Button('replace menu', classes='text-white bg-grey-7', events={'click': switch_menu})])

run(layout, menu=menu)
