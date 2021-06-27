from quasargui import *
accepted = Model(False)
layout = InputBool("Accept conditions", accepted)


def notify_if_accepted():
    if accepted.value:
        accepted.api.plugins.notify('Thanks for accepting!')


accepted.add_callback(notify_if_accepted)
run(layout)
