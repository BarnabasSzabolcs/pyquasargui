"""
This is a starter template.
"""

import quasargui
from quasargui import Model
from quasargui._layout import Toolbar, ToolbarTitle
from quasargui.callbacks import toggle
from quasargui.components import Layout, Header, Footer, Page, Drawer, Button

loading = Model(True)


def set_loaded():
    loading.value = False


layout = Layout([
    Header([
        Toolbar([ToolbarTitle(['Your Program Title'])])
    ]),
    Drawer([
        '<b class="q-mt-md">'
        '   Your drawer'
        '</b>'
        '<div class="q-mt-md">'
        'for your parameters.'
        '</div>'
    ]),
    Drawer(side=Drawer.RIGHT, show=False, children=[
        '<b class="q-mt-md">Your right drawer.</b>'
        '<div class="q-mt-md">'
        'If you comment out the right drawer, the right sandwich menu disappears'
        '</div>'
    ]),
    Page([
        'Here comes the contents of your Page'
    ]),
    Footer(show=loading, children=[
        'Here is your footer that is only displayed if the page is loading...',
        Button('ok', events={'click': toggle(loading)})
    ])
])

quasargui.run(layout, debug=True)
