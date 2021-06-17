from quasargui import *

is_large = Model(True)


def get_classes(ref):
    return [
        ' (class="',
        JSRaw("ref('{ref}') ? ref('{ref}').attributes.class.value : ''".format(ref=ref)),
        '")'
    ]


text_sm_lg = Div(
    classes='text-lg',
    props={
        'class': Computed(lambda x: '' if x else 'text-sm', is_large),
        'ref': 'sm_lg'
    },
    children=[
        'This text is ',
        Computed(lambda x: 'large' if x else 'small, luckily', is_large),
        *get_classes('sm_lg')
    ])

text_lg_sm = Div(
    classes='text-sm',
    props={
        'class': Computed(lambda x: 'text-lg' if x else '', is_large),
        'ref': 'lg_sm'
    },
    children=[
        Computed(lambda x: 'This text "should" be large too, but it is not' if x else 'This text is small', is_large),
        *get_classes('lg_sm')
    ])

text_no_conflict = Div(
    props={
        'class': Computed(lambda x: 'text-lg' if x else 'text-sm', is_large),
        'ref': 'no_conflict'
    },
    children=[
        'This text is ',
        Computed(lambda x: 'large' if x else 'small', is_large),
        *get_classes('no_conflict')
    ])

layout = Layout([Page(classes='q-ma-lg easyread', children=[
    Heading(5, 'Dynamic vs static classes'),
    "Be careful not to mix classes with overlapping meanings. <br>" 
    "Props's class always comes second in class html attribute.",
    Rows(row_classes='justify-left', classes='q-gutter-y-sm q-my-sm', children=[
        text_sm_lg,
        text_lg_sm,
        text_no_conflict
    ]),
    Toggle('Make text large', is_large, props={'left-label': True})
])])

run(layout, 'static vs dynamic classes', debug=True, _render_debug=True)
