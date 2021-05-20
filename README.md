# Python Quasar GUI
A modern, easy-to-use package for making Python GUI desktop apps.

### Usage:

Hello world: :)

    import quasargui
    from quasargui.components import Layout

    layout = Layout(children=["Hello World!"])
    quasargui.run(layout)

Hello {name}: Note that for all the components you can use all the classes and props described in (https://quasar.dev). AND you can also use css styling.

    import quasargui
    from quasargui.components import Layout, Input, Button

    def run_program():
        layout.notify(f'Hello, {input_name.value}!')

    input_name = Input()
    btn_submit = Button(
        label='Submit',
        classes='text-primary',
        props={'unelevated': True, 'size': 'lg'},
        events={'click': run_program})

    layout = Layout(
        styles={
            'max-width': '30em',
            'margin-left': 'auto',
            'margin-right': 'auto',
        },
        classes='q-mt-xl text-center',
        children=[
            "What's your name?",
            input_name,
            btn_submit
    ])

    quasargui.run(layout)


See further examples in the (/examples) folder.


### Installation:

This project is available via pip:

    pip install quasargui

#### Dependencies: 

 * pywebview

#### License:

MIT license
