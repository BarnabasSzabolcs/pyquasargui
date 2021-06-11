"""
This example shows how to deal with "deep" models. (dict or list valued models)
"""
from quasargui import *

dic_model = Model({})

dic_model['color'] = '#aaa'

print(dic_model['color'].value)  # ~> #aaa

dic_model['data'] = []
dic_model['data'].value.append('Item 1')
print(dic_model['data'][0].value)  # ~> Item 0
try:
    print(dic_model['data'][1].value)  # raises IndexError
except IndexError:
    print("dic_model['data'][1] call raised index error")

print(dic_model.value)  # ~> {'color': '#aaa', 'data': ['Item 1']}

deep_model = Model({'deep': {'data': 'deep value'}})

print(deep_model['deep']['data'].value)  # ~> deep value (but this creates 2 extra models)
print(deep_model.value['deep']['data'])  # ~> deep value (this just retrieves the value)

my_model = deep_model['deep']['data']

layout = Layout([Page([
    Input('deep model', my_model, events={
        'keyup': lambda: layout.notify(f"Deep value is {my_model.value}")
    })
])])

run(layout, _render_debug=True, debug=True)
