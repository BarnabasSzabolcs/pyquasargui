# noinspection PyUnresolvedReferences
import base64

# noinspection PyUnresolvedReferences
from quasargui.base import Component
from quasargui.tools import merge_classes, build_props
from quasargui.typing import PropValueType, ClassesType, StylesType, EventsType, ChildrenType, PropsType


class Div(Component):
    component = 'div'

    def __init__(self,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        super().__init__(children, classes, styles, props, events)


class Rows(Div):
    defaults = {
        'classes': 'q-gutter-y-xs',
        'row_classes': 'justify-center'
    }

    def __init__(self,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 row_classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        classes = merge_classes(
            'column',
            classes or self.defaults.get('classes', '')
        )
        self.row_classes = merge_classes(
            'row',
            row_classes or self.defaults.get('row_classes', ''))
        children = self._wrap_children(children)
        super().__init__(children, classes, styles, props, events)

    def _wrap_children(self, children):
        result = []
        for child in children or []:
            if isinstance(child, Columns):
                wrapped_child = child
                wrapped_child.classes = merge_classes(
                    wrapped_child.classes,
                    self.row_classes)
            else:
                wrapped_child = Div(children=[child], classes=self.row_classes)
            result.append(wrapped_child)
        return result

    @property
    def children(self):
        return self._children

    def set_children(self, children: ChildrenType):
        super().set_children(self._wrap_children(children))


class Columns(Div):
    defaults = {
        'classes': 'q-gutter-x-xs'
    }

    def __init__(self,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 column_classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        classes = merge_classes(
            'row',
            classes or self.defaults.get('classes', '')
        )
        self.column_classes = merge_classes(
            'column',
            column_classes or self.defaults.get('column_classes', ''))
        children = self._wrap_children(children)
        super().__init__(children, classes, styles, props, events)

    def _wrap_children(self, children):
        result = []
        for child in children or []:
            if isinstance(child, Rows):
                wrapped_child = child
                wrapped_child.classes = merge_classes(
                    wrapped_child.classes,
                    self.column_classes)
            else:
                wrapped_child = Div(children=[child], classes=self.column_classes)
            result.append(wrapped_child)
        return result

    @property
    def children(self):
        return self._children

    def set_children(self, children: ChildrenType):
        super().set_children(self._wrap_children(children))


class Link(Component):
    """
    This is not a Quasar component, but it is definitely useful.
    Use this component to point to external links.
    eg. Link('google', 'google.com', children=[Icon('open_in_new')])
    """
    component = 'a'
    defaults = {
        'props': {
            'target': '_blank'
        },
        'classes': 'text-primary'
    }

    def __init__(self,
                 title: str = None,
                 href: PropValueType[str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 children: ChildrenType = None,
                 events: EventsType = None):
        if children is None and title is None:
            raise AssertionError('either title or children parameter must be set')
        props = build_props(self.defaults['props'], {'href': href})
        if props['target'] == '_blank' and children is None:
            children = [Icon('open_in_new')]
        if title is not None:
            children = [title] + (children or [])
        classes = merge_classes(self.defaults['classes'], classes or '')
        super().__init__(children=children, props=props, classes=classes, styles=styles, events=events)


class Heading(Component):
    def __init__(self,
                 n: int,
                 text: PropValueType[str] = None,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 events: EventsType = None
                 ):
        if not 1 <= n <= 6:
            raise AssertionError('n must be between 1 and 6')
        self.component = f'h{n}'
        if text is not None:
            children = [text] + (children or [])
        super().__init__(children=children, classes=classes, styles=styles, events=events)


########################
# Some Quasar components
########################


class Button(Component):
    """
    ref. https://quasar.dev/vue-components/button#qbtn-api
    """
    component = 'q-btn'
    defaults = {
        'props': {
            'unelevated': True,
        }
    }

    # noinspection PyShadowingBuiltins
    def __init__(self,
                 label: PropValueType[str] = None,
                 icon: PropValueType[str] = None,
                 color: PropValueType[str] = None,
                 type: PropValueType[str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: ChildrenType = None):
        props = build_props({}, props, {
            'label': label,
            'icon': icon,
            'color': color,
            'type': type
        })
        super().__init__(classes=classes, styles=styles, props=props, events=events, children=children)


class Icon(Component):
    component = 'q-icon'

    def __init__(self,
                 name: PropValueType[str],
                 size: PropValueType[str] = None,
                 color: PropValueType[str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 events: EventsType = None,
                 children: ChildrenType = None):
        props = build_props({}, {}, {
            'name': name,
            'size': size,
            'color': color
        })
        super().__init__(
            props=props,
            classes=classes,
            styles=styles,
            events=events,
            children=children
        )


class PopupProxy(Component):
    component = 'q-popup-proxy'


class Spinner(Component):
    """

    appearances:
    https://quasar.dev/vue-components/spinners#example--other-spinners
    """
    component = 'q-spinner'
    appearances = {
        'audio', 'ball', 'bars', 'box', 'clock', 'comment', 'cube',
        'dots', 'facebook', 'gears', 'grid', 'hearts', 'hourglass',
        'infinity', 'ios', 'orbit', 'oval', 'pie', 'puff', 'radio',
        'rings', 'tail'}

    def __init__(self, appearance: str = None,
                 color: PropValueType[str] = None,
                 size: PropValueType[str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 ):
        kwargs = dict(
            props=build_props({}, props, {
                'color': color,
                'size': size
            }),
            classes=classes,
            styles=styles,
            events=events,
        )
        if appearance is not None:
            if appearance not in self.appearances:
                raise AssertionError(f'Appearance must be one of {self.appearances}')
            kwargs['component'] = f'q-spinner-{appearance}'
        super().__init__(**kwargs)


class Splitter(Component):
    """
    reference: https://quasar.dev/vue-components/splitter
    """
    component = 'q-splitter'


class Tooltip(Component):
    """
    reference: https://quasar.dev/vue-components/tooltip
    """
    component = 'q-tooltip'


class Tree(Component):
    """
    reference: https://quasar.dev/vue-components/tree
    """
    component = 'q-tree'
