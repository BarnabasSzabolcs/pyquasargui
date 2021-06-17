import json
from typing import TYPE_CHECKING

from quasargui.base import Component
from quasargui.components import Bar, Menu, QList, Button, QItem, QItemSection, Icon, Separator
from quasargui.typing import MenuSpecType

if TYPE_CHECKING:
    from quasargui.main import Api


def set_menu(api: 'Api', menuspec: MenuSpecType):
    menu = assemble_menu_bar(menuspec)
    menu.set_api(api)
    api.window.evaluate_js('app.setMenu({component})'.format(
        component=json.dumps(menu.vue)
    ))


def assemble_menu_bar(menuspec: MenuSpecType) -> Bar:
    return Bar([
        assemble_top_menu(spec) for spec in menuspec
    ])


def assemble_top_menu(spec) -> Component:
    props = {
        'stretch': True,
        'no-caps': True,
        'size': 'md',
        'padding': 'sm'
    }
    classes = 'q-pa-none'
    styles = {
        'font-weight': '400'
    }
    if 'children' in spec:
        return Button(
            props=props,
            classes=classes,
            styles=styles,
            children=[
                spec['title'],
                assemble_menu(spec['children'], top_level=True)
            ]
        )
    else:
        return Button(
            props=props,
            classes=classes,
            styles=styles,
            events={'click': spec['action']} if 'action' in spec else None,
            children=[spec['title']]
        )


def assemble_menu(menuspec: MenuSpecType, top_level: bool = False) -> Component:
    def get_item(spec):
        if not spec:
            return Separator()
        elif 'children' in spec:
            return QItem(
                props={
                    'clickable': True,
                },
                children=[
                    QItemSection([spec['title']]),
                    QItemSection(
                        props={'side': True},
                        children=[Icon('keyboard_arrow_right')]
                    ),
                    assemble_menu(spec['children'])
                ])
        else:
            return QItem(
                props={
                    'clickable': True,
                    'v-close-popup': None
                },
                children=[
                    QItemSection([spec['title']])
                ],
                events={'click': spec['action']} if 'action' in spec else None)
    if top_level:
        props = {
            # 'offset': [0, 0]
        }
    else:
        props = {
            'anchor': 'top end',
            'self': 'top start'
        }
    return Menu(
        props=props,
        children=[QList(
            props={'dense': True},
            styles={'min-width': '100px'},
            children=[get_item(spec) for spec in menuspec]
        )])
