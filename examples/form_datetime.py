from quasargui import *

layout = QLayout([QPage(classes='easyread q-my-lg', children=[
    Heading(4, 'Time, Date and DateTime'),
    InputDate('My birthday'),
    InputTime('Work starts usually at'),
    InputDateTime('Experiment started'),
])])

run(layout, size=(700, 700))
