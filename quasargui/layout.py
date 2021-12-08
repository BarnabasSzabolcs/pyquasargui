"""
This module contains all the Quasar elements that help with the general layout of the page.
"""

from typing import List, Union

from quasargui.base import Component, ComponentWithModel
from quasargui.callbacks import toggle
from quasargui.model import Model, Reactive
from quasargui.quasar_components import QButton
from quasargui.tools import merge_classes, build_props
from quasargui.typing import EventsType, ClassesType, StylesType, PropsType, ChildrenType, PropValueType


class QLayout(Component):
    """
    see: https://quasar.dev/layout-builder
    """
    component = 'q-layout'

    def __init__(self,
                 children: List[Union['QHeader', 'QDrawer', 'QPage', 'QFooter']] = None,
                 view: str = "hHh lpR fFf",
                 props: PropsType = None,
                 events: EventsType = None
                 ):
        """
        :param view: see layout-builder, the default value is good for most cases
        :param props:
        """
        props = props or {}
        props['view'] = props.get('view', view)
        children = self.build_children(children)
        super().__init__(children=children, props=props, events=events)

    @staticmethod
    def build_children(children):
        sandwich_menus = {}
        header = None
        for child in children:
            if isinstance(child, QDrawer):
                if child.menu_in_header:
                    sandwich_menus[child.props['side']] = child.model
            if isinstance(child, QHeader):
                header = child

        if header is not None and sandwich_menus:
            target = header.children[0] if isinstance(header.children[0], QToolbar) else header
            for side, model in sandwich_menus.items():
                menu_btn = QButton(
                    icon='menu',
                    classes='float-right' if side == QDrawer.RIGHT else '',
                    props={'dense': True},
                    events={'click': toggle(model)}
                )
                target.set_children(
                    [menu_btn, *target.children] if side == QDrawer.LEFT
                    else [*target.children, menu_btn])
        return children
    # TODO: we could have here a set_page() function that corresponds to the route's on a webpage.


class QHeader(ComponentWithModel):
    """
    q-header
    Use it within a QLayout.
    ref. https://quasar.dev/layout/header-and-footer#qheader-api
    """
    component = 'q-header'
    PRIMARY = 'bg-primary text-white'  # convenience constant

    defaults = {
        'props': {
            'reveal': False,  # this is hide_on_scroll
            'elevated': False,
            'bordered': False,
        }
    }

    def __init__(self,
                 children: ChildrenType = None,
                 hide_on_scroll: bool = None,  # this is the reveal prop
                 elevated: bool = None,
                 bordered: bool = None,
                 show: PropValueType[bool] = True,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None
                 ):
        if 1 <= len(children) <= 2 and isinstance(children[-1], str):
            children = [QToolbar([QToolbarTitle(children)])]

        props = build_props({}, props, {
            'reveal': hide_on_scroll,
            'elevated': elevated,
            'bordered': bordered,
        })
        model = show if isinstance(show, Reactive) else Model(show)
        super().__init__(model=model, children=children, classes=classes, styles=styles, props=props)


class QDrawer(ComponentWithModel):
    """
    q-drawer
    Use it within a QLayout.
    ref. https://quasar.dev/layout/drawer#qdrawer-api
    """
    component = 'q-drawer'
    # side constants
    LEFT = 'left'
    RIGHT = 'right'
    # behavior constants
    DESKTOP = 'desktop'
    MOBILE = 'mobile'
    RESPONSIVE = 'default'

    defaults = {
        'props': {
            'behavior': DESKTOP,
            'overlay': False,
            'bordered': True,
            'side': LEFT,
            'width': 200,
        }
    }

    def __init__(self,
                 children: ChildrenType = None,
                 menu_in_header: bool = True,
                 side: str = None,
                 show: Union[Model, bool] = True,
                 bordered: bool = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None
                 ):
        """
        :menu_in_header: if used together with QLayout, it instructs to put a close menu into the header.
        """
        self.menu_in_header = menu_in_header
        children = children
        props = build_props({}, props, {
            'side': side,
            'bordered': bordered,
        })
        model = show if isinstance(show, Reactive) else Model(show)
        super().__init__(model=model, children=children, classes=classes, styles=styles, props=props, events=events)


class QPage(Component):
    """
    q-page wrapped in q-page-container
    Use it within a QLayout.
    every parameter applies to the q-page.
    """
    component = 'q-page-container'
    defaults = {
        'props': {
            'padding': True,
        }
    }

    def __init__(self,
                 children: ChildrenType = None,
                 padding: PropValueType[bool] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None
                 ):
        props = build_props({}, props, {'padding': padding})
        self.page = _Page(children=children, classes=classes, styles=styles, props=props, events=events)
        super().__init__(children=[self.page])


class _Page(Component):
    """
    Internal component for the QPage,
    since in quasar q-page is always wrapped into q-page-container.
    """
    component = 'q-page'

    def __init__(self,
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None
                 ):
        super().__init__(children=children, classes=classes, styles=styles, props=props, events=events)


class QFooter(ComponentWithModel):
    """
    q-footer
    ref. https://quasar.dev/layout/header-and-footer#qfooter-api
    """
    component = 'q-footer'
    defaults = {
        'props': {
            'reveal': False,
            'elevated': False,
            'bordered': True,
            'show': True,
        },
        'classes': 'bg-white text-black q-px-sm'
    }

    def __init__(self,
                 children: ChildrenType = None,
                 show: PropValueType[bool] = None,
                 hide_on_scroll: bool = None,  # this is the reveal prop
                 elevated: bool = None,
                 bordered: bool = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None
                 ):
        props = build_props(self.defaults['props'], props, {
            'reveal': hide_on_scroll,
            'elevated': elevated,
            'bordered': bordered,
            'show': show,
        })
        show = props['show']
        model = show if isinstance(show, Reactive) else Model(show)
        super().__init__(model=model, children=children, classes=classes, styles=styles, props=props, events=events)


class QToolbar(Component):
    component = 'q-toolbar'


class QToolbarTitle(Component):
    component = 'q-toolbar-title'


class QSpace(Component):
    component = 'q-space'


class QBreadcrumbsElement(Component):
    """
    ref. https://quasar.dev/vue-components/breadcrumbs#qbreadcrumbsel-api
    """
    component = 'q-breadcrumbs-el'


class QBreadcrumbs(Component):
    """
    ref. https://quasar.dev/vue-components/breadcrumbs#qbreadcrumbs-api
    """
    component = 'q-breadcrumbs'

    def __init__(self,
                 children: List[QBreadcrumbsElement] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        super().__init__(
            children=children,
            classes=classes,
            styles=styles,
            props=props,
            events=events)


class QBar(Component):
    """
    ref. https://quasar.dev/vue-components/bar#qbar-api
    """
    component = 'q-bar'
