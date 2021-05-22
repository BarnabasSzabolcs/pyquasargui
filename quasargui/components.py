# noinspection PyUnresolvedReferences
from ._base import Model, Component, ComponentWithModel
# noinspection PyUnresolvedReferences
from ._layout import Header, Drawer  # , Page, Footer
from .typing import *


def flatten(lst) -> list:
    return [item for sublist in lst for item in sublist]


def merge_classes(*args) -> str:
    if len(args) == 1:
        return ' '.join(args[0]) if isinstance(args[0], list) else args[0]
    elif len(args) == 0:
        return ''
    else:
        return (merge_classes(args[0]) + ' ' + merge_classes(*args[1:])).strip()


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


class Input(ComponentWithModel):
    def __init__(self,
                 value: str = None,
                 model: Model = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        super().__init__(model=model, value=value, classes=classes, styles=styles, props=props, events=events)

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-input',
        })


class Button(Component):
    def __init__(self,
                 label: str = '',
                 icon: str = '',
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        props = props or {}
        if label and 'label' not in props:
            props['label'] = label
        if icon and 'icon' not in props:
            props['icon'] = icon
        super().__init__(classes=classes, styles=styles, props=props, events=events)

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-btn'
        })


class Plot(Component):
    pass
