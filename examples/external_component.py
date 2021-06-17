"""
A script is imported only once, automatically, before its component is first used.
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


model = Model(3)
layout = Layout([
    Page([
        MyComponent([
            'This is my basic component, written in python, also importing some external script.',
            Div(['external value: ', JSRaw('externalValue')])
        ]),
        MyWrappedComponent(model),
    ])
])

run(layout, debug=True, _render_debug=True)
