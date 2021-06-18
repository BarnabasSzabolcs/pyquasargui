import quasargui
from quasargui import *

a = Model(0)
b = Model(0)
even = Computed(lambda x, y: (x+y) % 2 == 0, a, b)
odd = Computed(lambda x: not x, even)

layout = Rows([
    QInput('a', model=a),
    '+',
    QInput('b', model=b),
    v_if(even, Div(['is even'])),
    v_if(odd, Div(['is odd'])),
])

quasargui.run(layout)
