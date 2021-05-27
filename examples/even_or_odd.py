import quasargui
from quasargui.callbacks import bind
from quasargui.components import *

a = Model(0)
b = Model(0)

layout = Rows([
    Input('a', model=a),
    Input('b', model=b),
    Div(props={'v-if': bind(lambda x, y: x+y % 2 == 0, a, b)}, children=[
        'even'
    ]),
    Div(props={'v-if': bind(lambda x, y: x+y % 2 != 0, a, b)}, children=[
        'odd'
    ]),
])

quasargui.run(layout)
