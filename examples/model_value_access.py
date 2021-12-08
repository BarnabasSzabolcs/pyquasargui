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

normal_model = Model('normal')

deep_model = Model({'deep': {'data': 'deep value'}})
print(deep_model['deep']['data'].value)  # ~> deep value (but this creates 2 extra models)
print(deep_model.value['deep']['data'])  # ~> deep value (this just retrieves the value)
deep_data = deep_model['deep']['data']

list_model = Model(['apple', 'orange'])
list0 = list_model[0]

layout = QLayout([QPage([
    QInput('normal:', normal_model, events={
        'keyup': lambda: layout.notify("Value is {}".format(normal_model.value))
    }),
    QInput('deep.data:', deep_data, events={
        'keyup': lambda: layout.notify("Value is {}".format(deep_data.value))
    }),
    QInput('list[0]:', list0, events={
        'keyup': lambda: layout.notify("Value is {}".format(list0.value))
    }),
])])

run(layout, _render_debug=True, debug=True)
