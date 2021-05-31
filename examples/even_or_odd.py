import quasargui
from quasargui import *

a = Model(0)
b = Model(0)
even = Computed(lambda x, y: (x+y) % 2 == 0, a, b)
odd = Computed(lambda x: not x, even)

layout = Rows([
    Input('a', model=a),
    '+',
    Input('b', model=b),
    Div(props={'v-if': even}, children=[
        'is even'
    ]),
    Div(props={'v-if': odd}, children=[
        'is odd'
    ]),
])

quasargui.run(layout)
