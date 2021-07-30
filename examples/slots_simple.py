from quasargui import *

layout = QInput(
    classes='q-ma-lg',
    label='Your city',
    children=[
        Slot('prepend', [
            QIcon('place')
        ])
    ])

run(layout, title='slots example')
