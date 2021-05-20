# Python Quasar GUI
A modern, easy-to-use package for making Python GUI desktop apps.

### Usage:

This GUI library builds up a window with a html view, in which Quasar Vue system is running. But don't worry, you can build up everything in python.

A window is build up of Components and the components correspond exactly to the components described in (https://quasar.dev/vue-components/). Quasar is very well-documented and so it makes this project well-documented. From Quasar's help page you can use all props, classes, as well as you can easily customize the look of your Components using CSS.

When the user does something you can execute your code based on callbacks. (See: simple greeter app.)

**Hello world:**

```python
import quasargui
from quasargui.components import Layout

layout = Layout(children=["Hello World!"])
quasargui.run(layout)
```

**Simple greeter app:**

This app demonstrates how you can build up a simple form and use the form's data to run your code.

```python
import quasargui
from quasargui.components import Layout, Input, Button

def display_notification():
    layout.notify(f'Hello, {input_name.value}!')

input_name = Input()  # see https://quasar.dev/vue-components/input#qinput-api
btn_submit = Button(  # see https://quasar.dev/vue-components/button#qbtn-api
    label='Submit',
    classes='text-primary',
    props={'unelevated': True, 'size': 'lg'},
    events={'click': display_notification})  # events are handled by callbacks

layout = Layout(  # a simple way of organizing the components vertically.
    styles={'max-width': '30em', 'margin-left': 'auto', 'margin-right': 'auto'},
    classes='q-mt-xl text-center',
    children=[
        "What's your name?",  # children can be components or strings, html is allowed.
        input_name,
        btn_submit
])

quasargui.run(layout)  # Shows a window with the layout.
```


See further examples in the (/examples) folder.


### Installation:

At the moment this project is just a demo, featuring only a few components,
but it will be available on pip soon.

#### Dependencies: 

 * pywebview

#### License:

MIT license
