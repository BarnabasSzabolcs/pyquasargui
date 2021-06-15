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


layout = Div(classes='text-center q-ma-lg',
             children=['Click on a menu'])

run(layout, menu=menu)
