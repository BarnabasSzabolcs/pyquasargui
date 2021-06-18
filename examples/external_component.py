"""
(A script is imported only once, automatically, before its component is first used.)
"""
from quasargui import *

this_dir = dirname(__file__)


class MyComponent(Component):
    script_sources = [join(this_dir, 'external_script.js')]
    style_sources = [join(this_dir, 'external_style.css')]
    defaults = {
        'classes': 'my-component'
    }


class MyWrappedComponent(ComponentWithModel):
    script_sources = [join(this_dir, 'external_script.js')]
    style_sources = [join(this_dir, 'external_style.css')]
    component = 'my-custom-component'


class MySingleFileComponent(SingleFileComponent):
    vue_source = join(this_dir, 'external_vue.vue')


model = Model(3)
layout = QLayout([
    QPage([
        MyComponent([
            Heading(5, 'MyComponent', classes='q-my-sm'),
            'written in python, also importing some external script.',
            Div([
                'value of externalValue: ',
                JSRaw('externalValue'),
                ' (externalValue is a variable in external_script.js)'])
        ]),
        MyWrappedComponent(model),
        MySingleFileComponent(props={'value': model})
    ])
])

run(layout, title='External component demonstration')
