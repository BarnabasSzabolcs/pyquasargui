"""
ref. https://quasar.dev/vue-components/tree#customize-content
"""

from quasargui import *

customize = Model([
    {
        'label': 'Satisfied customers',
        'header': 'root',
        'children': [
            {
                'label': 'Good food',
                'icon': 'restaurant_menu',
                'header': 'generic',
                'children': [
                    {
                        'label': 'Quality ingredients',
                        'header': 'generic',
                        'body': 'story',
                        'story': 'Lorem ipsum dolor sit amet.'
                    },
                    {
                        'label': 'Good recipe',
                        'body': 'story',
                        'story': 'A Congressman works with his equally conniving wife to exact revenge '
                                 'on the people who betrayed him.'
                    }
                ]
            },
            {
                'label': 'Good service',
                'header': 'generic',
                'body': 'toggle',
                'caption': 'Why are we as consumers so captivated by stories of great customer service? '
                           'Perhaps it is because...',
                'enabled': False,
                'children': [
                    {'label': 'Prompt attention'},
                    {'label': 'Professional waiter'}
                ]
            },
            {
                'label': 'Pleasant surroundings',
                'children': [
                    {'label': 'Happy atmosphere'},
                    {'label': 'Good table presentation', 'header': 'generic'},
                    {'label': 'Pleasing decor'}
                ]
            }
        ]
    }
])

layout = Tree(
    props={
        'nodes': customize,
        'node-key': 'label',
        'default-expand-all': True
    }, children=[
        Slot('default-header', lambda prop: [
            Div(classes='row items-center', children=[
                Icon(
                    # name=Computed(lambda ic: ic or 'share', prop['node']['icon']),
                    name=JSRaw(prop['node']['icon'].js_var_name + " || 'share'"),
                    size='28px',
                    color='orange',
                    classes='q-mr-sm'),
                Div(classes='text-weight-bold text-primary', children=[
                    prop['node']['label']
                ])
            ])
        ]),
        Slot('default-body', lambda prop: [
            Div(props={'v-if': prop['node']['story']}, children=[
                CustomComponent('span', classes='text-weight-bold', children=['This node has a story']),
                ': ',
                prop['node']['story']
            ]),
            CustomComponent('span', props={'v-else': None}, classes='text-weight-light text-black', children=[
                'This is some default content.'
            ])
        ])
    ])

run(layout, title='PropVar demo')
