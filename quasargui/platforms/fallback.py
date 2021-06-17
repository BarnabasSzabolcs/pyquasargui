import json
from typing import TYPE_CHECKING

from quasargui.base import Component
from quasargui.components import Bar, Menu, QList, Button, QItem, QItemSection, Icon, Separator, Tooltip
from quasargui.typing import MenuSpecType

if TYPE_CHECKING:
    from quasargui.main import Api


def set_menu(api: 'Api', menuspec: MenuSpecType):
    if not menuspec:
        api.window.evaluate_js('app.setMenu(false)')
        return
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
        if 'key' in spec:
            tooltip = [Tooltip([
                '(Ctrl{shift}+{key})</span>'.format(
                    shift='+Shift' if spec['key'].isupper() else '',
                    key=spec['key'].upper()
                )
            ])]
        else:
            tooltip = []
        button = Button(
            props=props,
            classes=classes,
            styles=styles,
            events={'click': spec['action']} if 'action' in spec else None,
            children=[spec['title']] + tooltip
        )
        if 'key' in spec:
            button.dependents.append(
                lambda api: api.set_key_shortcut(spec['key'], spec['action']))
        return button


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
                    QItemSection([Icon('keyboard_arrow_right')], props={'side': True}),
                    assemble_menu(spec['children'])
                ])
        else:
            children = [
                QItemSection([spec['title']])
            ]
            if 'key' in spec:
                shortcut_indicator = QItemSection(
                    props={'side': True},
                    children=[
                        'Ctrl{shift}+{key}'.format(
                            shift='' if spec['key'].islower() else '+Shift',
                            key=spec['key'].upper())
                    ]
                )
                shortcut_indicator.dependents.append(
                    lambda api: api.set_key_shortcut(spec['key'], spec['action']))
                children += [shortcut_indicator]

            return QItem(
                props={
                    'clickable': True,
                    'v-close-popup': None
                },
                children=children,
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
