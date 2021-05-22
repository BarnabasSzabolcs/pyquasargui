from typing import List, Union

from ._base import Component, Model, ComponentWithModel
from .typing import EventsType, ClassesType, StylesType, PropsType, ChildrenType


class Layout(Component):
    """
    q-layout
    see: https://quasar.dev/layout-builder
    """
    def __init__(self,
                 view: str = "hHh lpR fFf",
                 children: List[Union['Header', 'Drawer', 'Page', 'Footer']] = None,
                 props: PropsType = None
                 ):
        """
        :param view: see layout-builder, the default value is good for most cases
        :param props:
        """
        props = props or {}
        props['view'] = props.get('view', view)
        super().__init__(children=children, props=props)

    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-layout'
        })

    # TODO: we could have here a set_page() function that corresponds to the route's on a webpage.


class Header(ComponentWithModel):
    """
    q-header
    Use it within a Layout.
    """
    primary = 'bg-primary text-white'  # convenience class

    def __init__(self,
                 children: ChildrenType = None,
                 hide_on_scroll: bool = False,  # this is the reveal prop
                 elevated: bool = True,
                 bordered: bool = False,
                 show: Union[Model, bool] = True,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None
                 ):
        children = children
        props = props or {}
        props['reveal'] = props.get('reveal', hide_on_scroll)
        props['elevated'] = props.get('elevated', elevated)
        props['bordered'] = props.get('bordered', bordered)
        model = show if isinstance(show, Model) else Model(show)
        super().__init__(model=model, children=children, classes=classes, styles=styles, props=props)

    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-header'
        })


class Drawer(ComponentWithModel):
    """
    q-drawer
    Use it within a Layout.
    """
    # side constants
    LEFT = 'left'
    RIGHT = 'right'

    def __init__(self,
                 side: str = LEFT,
                 children: ChildrenType = None,
                 show: Union[Model, bool] = None,
                 bordered: bool = True,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None
                 ):
        children = children
        props = props or {}
        model = show if isinstance(show, Model) else Model(show)
        props['side'] = props.get('side', side)
        props['bordered'] = props.get('bordered', bordered)
        super().__init__(model=model, children=children, classes=classes, styles=styles, props=props, events=events)

    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-drawer'
        })


class Page(Component):
    """
    q-page wrapped in q-page-container
    Use it within a Layout.
    every parameter applies to the q-page.
    """
    def __init__(self,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None
                 ):
        self.page = _Page(children=children, classes=classes, styles=styles, props=props, events=events)
        super().__init__(children=[self.page])

    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-page-container'
        })


class _Page(Component):
    """
    Internal component for the Page,
    since in quasar q-page is always wrapped into q-page-container.
    """
    def __init__(self,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None
                 ):
        super().__init__(children=children, classes=classes, styles=styles, props=props, events=events)

    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-page'
        })


class Footer(ComponentWithModel):
    def __init__(self,
                 children: ChildrenType = None,
                 show: Union[Model, bool] = True,
                 hide_on_scroll: bool = False,  # this is the reveal prop
                 elevated: bool = True,
                 bordered: bool = False,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None
                 ):
        children = children
        props = props or {}
        props['reveal'] = props.get('reveal', hide_on_scroll)
        props['elevated'] = props.get('elevated', elevated)
        props['bordered'] = props.get('bordered', bordered)
        model = show if isinstance(show, Model) else Model(show)
        super().__init__(model=model, children=children, classes=classes, styles=styles, props=props, events=events)

    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-footer'
        })
