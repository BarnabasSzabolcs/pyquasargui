from quasargui import ComponentWithModel, Model, ClassesType, StylesType, PropsType, build_props


class VueTagsInput(ComponentWithModel):
    """
    see http://www.vue-tags-input.com/#/examples/hooks
    Note that model points to 'tags' property,
    'v-model' can be accessed via self.current_tag.
    """
    component = 'vue-tags-input'
    script_sources = ['vue-tags-input.2.1.0.js']
    style_sources = ['vue-tags-input.css']

    def __init__(self,
                 model: Model = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None):
        props = build_props({}, props, {
            'tags': model or Model([])
        })
        events = {
            'tags-changed': lambda new_tags: model.set_value(new_tags)
        }
        self.dependents = [props['tags']]
        self.current_tag = Model('')
        super().__init__(
            model=self.current_tag,
            props=props,
            classes=classes,
            styles=styles,
            events=events)
