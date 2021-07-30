from quasargui import *

few_choices = ['blonde', 'red', 'brown', 'blue', 'pink']
many_choices = [
    'blonde', 'red', 'brown', 'blue', 'pink',
    'black', 'grey', 'white', 'bold', 'long',
    'short', 'thin', 'thick', 'medium', 'rasta'
]

my_choice1 = Model('blonde')
my_choice2 = Model('blonde')
my_choice3 = Model('blonde')
my_choice4 = Model('blonde')
multi_choice1 = Model([])
multi_choice2 = Model([])
multi_choice3 = Model([])

gap_classes = 'q-pt-lg'

selected_tab = Model('single')

single_choice_components = [
    InputChoice(
        'my choice - no choice set',
        my_choice1,
        classes=gap_classes),
    InputChoice(
        'my choice', my_choice2,
        choices=few_choices,
        classes=gap_classes),
    InputChoice(
        'my choice - many choices',
        my_choice3,
        choices=many_choices,
        classes=gap_classes),
    InputChoice(
        'my choice - appearance=buttons',
        my_choice4,
        choices=few_choices,
        appearance='buttons',
        classes=gap_classes)
]

multiple_choice_components = [
    InputChoice(
        'multiple choices - no choice set',
        multi_choice1,
        classes=gap_classes,
        multiple=True),
    InputChoice(
        'my choice - a few choices set',
        multi_choice2,
        choices=few_choices,
        classes=gap_classes,
        multiple=True),
    InputChoice(
        'my choice - many choices set',
        multi_choice3,
        choices=many_choices,
        classes=gap_classes,
        multiple=True),
]

layout = QLayout([QPage(classes='easyread', children=[
    Heading(4, 'Input choice appearances', classes='q-mb-md'),
    QTabs(selected_tab, classes='text-primary', children=[
        QTab('single', label='single value'),
        QTab('multiple', label='multiple values')],
    ),
    QTabPanels(selected_tab, [
        QTabPanel('single', single_choice_components),
        QTabPanel('multiple', multiple_choice_components),
    ]),
])])

run(layout, 'Form - input choice demo', size=(600, 550), _render_debug=True, debug=True)
