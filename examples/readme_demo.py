from quasargui import *

check1 = Model(False)
check2 = Model(False)
check3 = Model(True)

QInput.defaults['props'] = {
    'outlined': True,
}

layout = QLayout([
    QHeader([QToolbar([
        QToolbarTitle(['QuasarGUI']),
        QSpace(),
        QButton(icon='language', props={'stretch': True}),
        QButton(icon='favorite', props={'stretch': True}),
    ])]),
    QPage([
        Heading(1, classes='q-mt-lg q-mb-none', children=[
            QImg('../../docs/assets/logo4.png', styles={'max-width': '200px'}),
            'QuasarGUI'
        ]),
        Div(classes='text-center', children=[
            QForm([
                Rows(classes='text-left q-gutter-lg', children=[
                    Columns([
                       QInput("Input a value", Model('fresh and groovy'))
                    ]),
                    Columns([
                        QCheckbox('one', check1),
                        QCheckbox('two', check2),
                        QCheckbox('three', check3),
                    ]),
                        Columns([
                        QButton('OK', classes='bg-primary text-white'),
                        QButton('Cancel')
                    ])
                ])
            ])
        ])
    ])
])

run(layout, debug=True, title='Python GUI framework - based on Quasar')