# Python Quasar GUI
A modern, easy-to-use package for making Python GUI desktop apps.

### Usage:

**Hello world:** the minimal implementation.
```python
import quasargui
from quasargui.components import Layout

layout = Layout(children=["Hello World!"])
quasargui.run(layout)
```
**Simple greeter app:** Note that for all the components you can use all the classes and props described in (https://quasar.dev). AND you can also use css styling.

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

This project is available via pip:

    pip install quasargui

#### Dependencies: 

 * pywebview

#### License:

MIT license
