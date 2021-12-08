from quasargui import *
from quasargui.vue_tags_input import VueTagsInput


def init_person():
    return {
        'name': '',
        'role': '',
        'office': 'New York',
        'experience': 0,
        'height': 100,
        'tags': []
    }


person = Model(init_person())
accept = Model(False)


def add_employee():
    if accept.value:
        person.api.plugins.notify(
            type='positive',
            icon='done',
            message='<b>Employee added!</b>\n'
                    'name: {name}\n'
                    'role: {role}\n'
                    'experience: {experience}\n'
                    'height: {height}\n'
                    'tags: {tags}'.format(**person.value))
        person.value = init_person()
    else:
        person.api.plugins.notify('Have to accept the terms.', type='negative', icon='report_problem')


label_classes = 'q-mr-md'

Columns.defaults['classes'] = ''

layout = QLayout([QPage([
    QForm(classes='easyread q-px-md q-py-lg', children=[
        Heading(4, 'Add Employee', classes='q-mb-md q-pt-lg'),
        QInput('name', person['name']),
        QSelect('role', person['role'], props={'options': ['Manager', 'Worker'], 'use-input': True}),
        QSelect('office', person['office'], props={'options': ['London', 'New York'], 'readonly': True, 'disabled': True}),
        Columns(classes='items-center', children=[
            Div(['experience:'], label_classes),
            QKnob(person['experience'], props={'min': 0, 'max': 10, 'step': 1}),
        ]),
        Columns(classes='items-center', children=[
            Div(['height:'], label_classes),
            QSlider(person['height'], props={'min': 100, 'max': 250, 'step': 1}, styles={'min-width': '200px'})
        ]),
        Columns(classes='items-center', children=[
            Div(['tags:'], label_classes),
            VueTagsInput(person['tags']),
        ]),
        Div([
            QCheckbox('accept terms', accept),
        ]),
        QButton('submit', events={'click': add_employee}, classes='bg-primary text-white')
    ])
])])

run(layout, 'Register employee', size=(500, 700))
