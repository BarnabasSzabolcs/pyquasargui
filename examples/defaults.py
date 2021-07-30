from quasargui import *

QButton.defaults['props'] = {
    'glossy': True,
    'color': 'orange',
    'rounded': True
}
QInput.defaults['props'] = {
    'outlined': True,
    'rounded': True
}

layout = Rows(classes='q-mt-lg q-gutter-md', children=[
    Columns([QButton('one'), QButton('two'), QButton('oranje!')]),
    QInput('me is outlined')
])

run(layout, title='We likes glossy', size=(300, 200))
