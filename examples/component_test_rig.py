from quasargui import *
model = Model([])
model.add_callback(lambda: model.api.plugins.notify(json.dumps(model.value)))
run(VueTagsInput(model), debug=True, _render_debug=True)
