from typing import List, Union

from quasargui.components import Component, ComponentWithModel
from quasargui.model import Model
from quasargui.form import Button
from quasargui.tools import merge_classes, build_props
from quasargui.callbacks import toggle
from quasargui.typing import EventsType, ClassesType, StylesType, PropsType, ChildrenType


class Layout(Component):
    """
    q-layout
    see: https://quasar.dev/layout-builder
    """
    def __init__(self,
                 children: List[Union['Header', 'Drawer', 'Page', 'Footer']] = None,
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

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-layout'
        })

    @staticmethod
    def build_children(children):
        sandwich_menus = {}
        header = None
        for child in children:
            if isinstance(child, Drawer):
                if child.menu_in_header:
                    sandwich_menus[child.props['side']] = child.model
            if isinstance(child, Header):
                header = child

        if header is not None and sandwich_menus:
            target = header.children[0] if isinstance(header.children[0], Toolbar) else header
            for side, model in sandwich_menus.items():
                menu_btn = Button(
                    icon='menu',
                    classes='float-right' if side == Drawer.RIGHT else '',
                    props={'dense': True},
                    events={'click': toggle(model)}
                )
                target.set_children(
                    [menu_btn, *target.children] if side == Drawer.LEFT
                    else [*target.children, menu_btn])
        return children
    # TODO: we could have here a set_page() function that corresponds to the route's on a webpage.


class Header(ComponentWithModel):
    """
    q-header
    Use it within a Layout.
    ref. https://quasar.dev/layout/header-and-footer#qheader-api
    """
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
                 show: Union[Model, bool] = True,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None
                 ):
        children = children
        props = build_props(
            defaults=self.defaults['props'],
            props=props,
            specials={
                'reveal': hide_on_scroll,
                'elevated': elevated,
                'bordered': bordered,
            })
        model = show if isinstance(show, Model) else Model(show)
        super().__init__(model=model, children=children, classes=classes, styles=styles, props=props)

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-header'
        })


class Drawer(ComponentWithModel):
    """
    q-drawer
    Use it within a Layout.
    ref. https://quasar.dev/layout/drawer#qdrawer-api
    """
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
        :menu_in_header: if used together with Layout, it instructs to put a close menu into the header.
        """
        self.menu_in_header = menu_in_header
        children = children
        props = build_props(
            defaults=self.defaults['props'],
            props=props,
            specials={
                'side': side,
                'bordered': bordered,
            })
        model = show if isinstance(show, Model) else Model(show)
        super().__init__(model=model, children=children, classes=classes, styles=styles, props=props, events=events)

    @property
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
    defaults = {
        'props': {
            'padding': True,
        }
    }

    def __init__(self,
                 children: ChildrenType = None,
                 padding: bool = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None
                 ):
        props = build_props(self.defaults['props'], props, {'padding': padding})
        self.page = _Page(children=children, classes=classes, styles=styles, props=props, events=events)
        super().__init__(children=[self.page])

    @property
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

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-page'
        })


class Footer(ComponentWithModel):
    """
    q-footer
    ref. https://quasar.dev/layout/header-and-footer#qfooter-api
    """
    defaults = {
        'props': {
            'reveal': False,
            'elevated': False,
            'bordered': True,
            'show': True,
        },
        'classes': 'bg-white text-black'
    }

    def __init__(self,
                 children: ChildrenType = None,
                 show: Union[Model, bool] = None,
                 hide_on_scroll: bool = None,  # this is the reveal prop
                 elevated: bool = None,
                 bordered: bool = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None
                 ):
        children = children
        props = build_props(
            defaults=self.defaults['props'],
            props=props,
            specials={
                'reveal': hide_on_scroll,
                'elevated': elevated,
                'bordered': bordered,
                'show': show,
            })
        classes = merge_classes(self.defaults['classes'], classes or '')
        show = props['show']
        model = show if isinstance(show, Model) else Model(show)
        super().__init__(model=model, children=children, classes=classes, styles=styles, props=props, events=events)

    @property
    def vue(self) -> dict:
        return self._merge_vue({
            'component': 'q-footer'
        })


class Toolbar(Component):
    component = 'q-toolbar'


class ToolbarTitle(Component):
    component = 'q-toolbar-title'


class Space(Component):
    component = 'q-space'


class Avatar(Component):
    component = 'q-avatar'


class Icon(Component):
    component = 'q-icon'

    def __init__(self,
                 name: Union[str, Model],
                 size: Union[str, Model] = None,
                 color: Union[str, Model] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None):
        props = build_props({}, {}, {'name': name, 'size': size, 'color': color})
        super().__init__(props=props, classes=classes, styles=styles)