import quasargui
from quasargui import set_main_component
from quasargui.components import Layout, Input, Rows, Button, Columns


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


buttons = [
    Button(
        text,
        props={'unelevated': True, 'color': 'primary'},
        styles={'min-width': '100px'},
    )
    for text in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
]


def update_text_list():
    try:
        i = int(input_number.value)
    except ValueError:
        layout.notify("Please enter digits", type='negative', icon='warning')
        input_number.value = ''
        return
    if i < 1 or i > 10:
        layout.notify("Number not in range", type='negative', icon='warning')
        input_number.value = ''
        return

    result_layout = Layout(children=[
        Columns(children=[Rows(children=row) for row in chunks(buttons[:i], 3)]),
        Button(
            label='back',
            classes='q-ma-sm',
            props={'unelevated': True, 'color': 'grey-7'},
            events={'click': lambda: set_main_component(layout)})
    ])
    set_main_component(result_layout)


input_number = Input(
    styles={'min-width': "30em"},
    props={'label': 'Enter a number between 1 and 10'},
    events={'change': update_text_list})
ok_btn = Button(
    label='ok',
    props={'unelevated': True, 'color': 'primary'},
    events={'click': update_text_list})

layout = Rows(
    classes='text-center',
    children=[
        '<h5>Dynamic components</h5>',
        input_number,
        Layout(
            props={'v-if': input_number.ref},
            classes="text-left q-ml-sm",
            children=["You have entered: ", input_number.ref]),
        ok_btn
    ])

quasargui.run(layout, debug=True)
