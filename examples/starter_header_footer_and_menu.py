"""
This is a starter template.
"""

import quasargui
from quasargui import *

loading = Model(True)


def set_loaded():
    loading.value = False


layout = QLayout([
    QHeader([
        QToolbar([QToolbarTitle([
            QIcon('ramen_dining', 'lg', classes='q-mx-md'),
            'Your Program Title'
        ])])
    ]),
    QDrawer([
        '<b>'
        'Your drawer'
        '</b>'
        '<div class="q-mt-md">'
        'for your parameters.'
        '</div>'
    ]),
    QDrawer(side=QDrawer.RIGHT, show=False, children=[
        '<b>'
        'Your right drawer.'
        '</b>'
        '<div class="q-mt-md">'
        'If you delete a drawer,its sandwich menu disappears'
        '</div>'
    ]),
    QPage([
        'Here comes the contents of your QPage'
    ]),
    QFooter(show=loading, children=[
        'Here is your footer that is only displayed if loading.value == True',
        QButton('ok', events={'click': toggle(loading)})
    ])
])

quasargui.run(layout, title='Program title')
