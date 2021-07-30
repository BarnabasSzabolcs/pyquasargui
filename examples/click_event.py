from quasargui import *

layout = QButton('Click me', events={'click': lambda: layout.api.plugins.notify("I've got clicked!")})
run(layout)
