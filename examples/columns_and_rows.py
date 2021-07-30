from quasargui import *

layout = QLayout([QPage([
    Columns(styles={'height': '100vh'}, column_classes='col-grow', children=[
        Rows(row_classes='bg-grey-1 row-grow align-center', children=[
            Div(['({}, {})'.format(i+1, j+1)]) for j in range(6)
        ])
        for i in range(4)
    ])
])])

run(layout, 'Columns and rows example', debug=True, size=(400, 300))
