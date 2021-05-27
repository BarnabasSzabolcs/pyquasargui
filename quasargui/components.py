# noinspection PyUnresolvedReferences
import base64

# noinspection PyUnresolvedReferences
from quasargui.base import Component

# noinspection PyUnresolvedReferences
from quasargui.form import *
# noinspection PyUnresolvedReferences
from quasargui.layout import *
# noinspection PyUnresolvedReferences
from quasargui.plot import *
from quasargui.tools import merge_classes
from quasargui.typing import *


class Div(Component):
    def __init__(self,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        super().__init__(children, classes, styles, props, events)

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'div'
        })


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
