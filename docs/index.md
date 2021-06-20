# QuasarGUI

Quasargui is a user-friendly package for making modern desktop apps in Python.

Some reasons you might want to use QuasarGUI:
1. It is built on a stable front-end framework, [Quasar](https://quasar.dev).
2. It brings the advantages of Vue
3. Still, you don't ever need to touch JavaScript code, everything is brought back to Python. 

## Hello World example

```python
from quasargui import *

name = Model('')
layout = Rows([
    QInput('Your name:', name),
    QButton('Submit', events={
        'click': lambda: layout.notify(
            message=f'Hello, {name.value}!', position='bottom')
    })
])
run(layout, title='Hello World program')
```
If we fill in "World" and click "Submit", this program outputs

![Hello World screenshot](assets/screenshots/quasar-gui-hello-world-screenshot.png "Hello World screenshot")

Let's break it down how it works.    
When we change `QInput`, `name`'s value is updated automatically. So, when we click on `QButton`, the callback function calls the window-wide fully-customizable `notify` with the correct name, `'World'`. 

`Rows`, `QInput`, and `QButton` (that internally correspond to Vue components) are the widgets. We communicate with Widgets there-and-back via `Model`'s. (That is, `Model`'s are two-way bound to the window.)

## List of examples

A range of examples can be found in the [examples directory on GitHub](https://github.com/BarnabasSzabolcs/pyquasargui/tree/develop/examples).
These examples we describe in detail.

### Styling Hello World

Components can be easily changed by adding a few css classes and styles.

You can see the (reference of the classes on quasar.dev)[https://quasar.dev/style/spacing#introduction], for spacing, positioning, typography, visibility and breakpoints and (shadows)[https://quasar.dev/style/shadows].


=== "Screenshot"
    ![examples/simple.py screenshot](assets/screenshots/simple.png "examples/simple.py screenshot")

=== "Code"

```python
from quasargui import *

name = Model('')
layout = Div(
    styles={
        'max-width': '30em',
        'margin-left': 'auto',
        'margin-right': 'auto',
    },
    classes='q-mt-xl text-center',
    children=[
        "What's your name?",
        QInput(model=name),
        QButton('Submit', 
                classes='text-primary',
                props={'unelevated': True, 'size': 'lg'},
                events={
                    'click': lambda: layout.notify(
                        f'Hello, {name.value}!', position='bottom')
        })
    ])
```

### Standard boilerplate



