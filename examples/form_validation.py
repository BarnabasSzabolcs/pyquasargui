import quasargui
from quasargui import *


def on_submit():
    validation = True
    validation = validation and input_name.validate()
    validation = validation and input_age.validate()
    if not accept.value:
        accept.api.plugins.notify(
            color='negative',
            message='You need to accept the license and terms first',
            icon='report_problem'
        )
    elif validation:
        accept.api.plugins.notify(
            icon='done',
            color='positive',
            message='Submitted'
        )


def on_reset():
    input_name.reset_validation()
    input_age.reset_validation()


QInput.defaults['props'].update({
    'filled': True,
    'lazy-rules': True
})


accept = Model(False)

input_name = QInput('Your name *', props={
    'hint': 'Name and surname',
    'rules': JSRaw("[ val => val && val.length > 0 || 'Please type something']")
})
input_age = QInput('Your age *', type='number', props={
    'rules': JSRaw("""[
              val => val !== null && val !== '' || 'Please type your age',
              val => val > 0 && val < 100 || 'Please type a real age'
            ]""")
})
validate_on_submit = QForm(
    styles={'max-width': '30em', 'margin': '0 auto'},
    events={
        'submit.prevent.stop': on_submit,
        'reset.prevent.stop': on_reset
    }, children=[
        Heading(5, 'Form validation on submit'),
        Div(classes='q-mb-md', children=[
            'Reference: ',
            Link('here', "https://quasar.dev/vue-components/input#example--form-validation")
        ]),
        input_name,
        input_age,
        QToggle('I accept the license and terms', accept),
        Columns([
            QButton('Submit', type='submit', color='primary', props={
                'unelevated': False
            }),
            QButton('Reset', type='reset', color='primary', props={
                'flat': True
            })
        ])
    ])

layout = QLayout([
    QHeader(['Form validation <small>- on submit</small>']),
    QPage([validate_on_submit])
])

quasargui.run(layout, 'Form validation demo', size=(600, 550))
