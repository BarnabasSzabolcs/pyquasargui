import quasargui
from quasargui.base import JSFunction
from quasargui.components import *
from quasargui.form import Form
from quasargui.layout import *


def on_submit():
    validation = True
    validation = validation and input_name.validate()
    validation = validation and input_age.validate()
    if not accept.value:
        accept.api.send_notification({
            'color': 'negative',
            'message': 'You need to accept the license and terms first'
        })
    elif validation:
        accept.api.send_notification({
            'icon': 'done',
            'color': 'positive',
            'message': 'Submitted'
        })


def on_reset():
    input_name.reset_validation()
    input_age.reset_validation()


Input.defaults['props'].update({
    'filled': True,
    'lazy-rules': True
})


accept = Model(False)

input_name = Input('Your name *', props={
    'hint': 'Name and surname',
    'rules': JSFunction("[ val => val && val.length > 0 || 'Please type something']")
})
input_age = Input('Your age *', type='number', props={
    'rules': JSFunction("""[
              val => val !== null && val !== '' || 'Please type your age',
              val => val > 0 && val < 100 || 'Please type a real age'
            ]""")
})
validate_on_submit = Form(
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
        Toggle('I accept the license and terms', accept),
        Columns([
            Button('Submit', type='submit', color='primary', props={
                'unelevated': False
            }),
            Button('Reset', type='reset', color='primary', props={
                'flat': True
            })
        ])
    ])

layout = Layout([
    Header(['Form validation <small>- on submit</small>']),
    Page([validate_on_submit])
])

quasargui.run(layout, debug=True)
