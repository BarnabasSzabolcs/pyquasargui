# noinspection PyUnresolvedReferences
import base64

# noinspection PyUnresolvedReferences
from quasargui.base import Component, LabeledComponent
from quasargui.quasar_components import QIcon
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
    eg. ``Link('google', 'google.com', children=[QIcon('open_in_new')])``
    """
    component = 'a'
    defaults = {
        'props': {
            'target': '_blank'
        },
        'classes': 'text-primary',
        'styles': {
            'text-decoration': 'none'
        }
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
        styles = build_props(self.defaults['styles'], styles)
        if props['target'] == '_blank' and children is None:
            children = [QIcon('open_in_new')]
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
        self.component = 'h{}'.format(n)
        if text is not None:
            children = [text] + (children or [])
        super().__init__(children=children, classes=classes, styles=styles, events=events)
