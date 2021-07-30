from typing import List, Union

from quasargui.base import Component, LabeledComponent, Model, Slot, ComponentWithModel
from quasargui.tools import build_props
from quasargui.typing import ClassesType, StylesType, PropsType, PropValueType, EventsType, ChildrenType


class QAvatar(Component):
    """
    ref. https://quasar.dev/vue-components/avatar#qavatar-api
    """
    component = 'q-avatar'


class QBadge(Component):
    """
    ref. https://quasar.dev/vue-components/badge#qbadge-api
    """
    component = 'q-badge'


class QBanner(Component):
    """
    ref. https://quasar.dev/vue-components/banner#qbanner-api
    """
    component = 'q-banner'


class QButton(Component):
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


class QButtonDropdown(Component):
    """
    Use it with QList
    ref. https://quasar.dev/vue-components/button-dropdown#qbtndropdown-api
    """
    component = 'q-btn-dropdown'
    defaults = {
        'props': {
            'unelevated': True,
        }
    }

    def __init__(self,
                 children: List[Union['QList', Slot]] = None,
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


class QButtonGroup(Component):
    """
    Use it with QButton and QButtonDropdown.
    ref. https://quasar.dev/vue-components/button-group#qbtngroup-api
    """
    component = 'q-btn-group'
    defaults = {
        'props': {
            'unelevated': True,
        }
    }

    def __init__(self,
                 children: List[Union[QButton, QButtonDropdown]] = None,
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


class QCard(Component):
    """
    ref. https://quasar.dev/vue-components/card#qcard-api
    Use it with QCardSection, QSeparator and QCardActions
    """
    component = 'q-card'

    def __init__(self,
                 children: List[Union['QCardSection', 'QSeparator', 'QCardActions']] = None,
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


class QCardSection(Component):
    """
    ref. https://quasar.dev/vue-components/card#qcardsection-api
    """
    component = 'q-card-section'


class QCardActions(Component):
    """
    ref. https://quasar.dev/vue-components/card#qcardactions-api
    """
    component = 'q-card-actions'


class QCarousel(Component):
    """
    Use it with QCarouselSlide and Slot('control', [QCarouselControl]).
    ref. https://quasar.dev/vue-components/carousel#qcarousel-api
    """
    component = 'q-carousel'

    def __init__(self,
                 children: List[Union['QCarouselSlide', Slot]] = None,
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


class QCarouselControl(Component):
    """
    ref. https://quasar.dev/vue-components/carousel#qcarouselcontrol-api
    """
    component = 'q-carousel-control'


class QCarouselSlide(Component):
    """
    ref. https://quasar.dev/vue-components/carousel#qcarouselslide-api
    """
    component = 'q-carousel-slide'


class QChatMessage(Component):
    """
    ref. https://quasar.dev/vue-components/chat#qchatmessage-api
    """
    component = 'q-chat-message'


class QChip(Component):
    """
    ref. https://quasar.dev/vue-components/chip#qchip-api
    """
    component = 'q-chip'


class QCircularProgress(ComponentWithModel):
    """
    ref. https://quasar.dev/vue-components/circular-progress#qcircularprogress-api
    """
    component = 'q-circular-progress'


class QDialog(ComponentWithModel):
    """
    ref. https://quasar.dev/vue-components/dialog#qdialog-api
    """
    component = 'q-dialog'


class QEditor(ComponentWithModel):
    """
    QEditor does not work for some reason :(

    ref. https://quasar.dev/vue-components/editor
    """
    component = 'q-editor'

    def __init__(self,
                 model: Model = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 children: List[Union[Slot]] = None,
                 events: EventsType = None):
        model = model or Model('')
        super().__init__(model=model, classes=classes, styles=styles, children=children, props=props, events=events)


class QExpansionItem(LabeledComponent):
    """
    Use it with ListComponent, children: QCard, and QCardSection within the QCard.
    ref. https://quasar.dev/vue-components/expansion-item#qexpansionitem-api
    """
    component = 'q-expansion-item'
    defaults = {
        'props': {
            'expand-separator': True
        }
    }


class QFab(LabeledComponent):
    """
    ref. https://quasar.dev/vue-components/floating-action-button#qfab-api
    """
    component = 'q-fab'

    def __init__(self,
                 label: str = None,
                 model: Model = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: List[Union['QFabAction', Slot]] = None):
        super().__init__(
            label=label,
            model=model,
            classes=classes,
            styles=styles,
            props=props,
            events=events,
            children=children)


class QFabAction(Component):
    """
    ref. https://quasar.dev/vue-components/floating-action-button#qfabaction-api
    """
    component = 'q-fab-action'


class QIcon(Component):
    component = 'q-icon'

    def __init__(self,
                 name: PropValueType[str],
                 size: PropValueType[str] = None,
                 color: PropValueType[str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 events: EventsType = None,
                 props: PropsType = None,
                 children: ChildrenType = None):
        props = build_props({}, props, {
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


class QImg(Component):
    """
    ref. https://quasar.dev/vue-components/img#qimg-api
    """
    component = 'q-img'

    def __init__(self,
                 src: PropValueType[str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: ChildrenType = None):
        props = build_props({}, props, {'src': src})
        super().__init__(classes=classes, styles=styles, props=props, events=events, children=children)


class QInfiniteScroll(Component):
    """
    ref. https://quasar.dev/vue-components/infinite-scroll#qinfinitescroll-api
    """
    component = 'q-infinite-scroll'


class QInnerLoading(Component):
    """
    Must be the last element in its parent's children list.
    It fades the parent component and displays a spinner (must be set as children parameter)
    eg.
    ::

        Component([
            ...
            QInnerLoading([QSpinner()], props={'showing': Model(True)})
        ])

    ref. https://quasar.dev/vue-components/inner-loading#qinnerloading-api
    """
    component = 'q-inner-loading'


class QIntersection(Component):
    """
    Use it inside a v_for.
    Displays nice transitions for a listing.
    children are typically QCard or QItem
    ref. https://quasar.dev/vue-components/intersection#qintersection-api
    """
    component = 'q-inner-loading'


# class QKnob is in quasar_form


class QList(Component):
    """
    ref. https://quasar.dev/vue-components/list-and-list-items#qlist-api
    """
    component = 'q-list'

    def __init__(self,
                 children: List['QItem'] = None,
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


class QItem(Component):
    """
    ref. https://quasar.dev/vue-components/list-and-list-items#qitem-api
    """
    component = 'q-item'

    def __init__(self,
                 children: List['QItemSection'] = None,
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


class QItemLabel(Component):
    """
    ref. https://quasar.dev/vue-components/list-and-list-items#qitemlabel-api
    """
    component = 'q-item-label'


class QItemSection(Component):
    """
    QItemLabel can be useful as child
    for example: https://quasar.dev/vue-components/list-and-list-items#basic

    ref. https://quasar.dev/vue-components/list-and-list-items#qitemsection-api
    """
    component = 'q-item-section'


class QMarkupTable(Component):
    """
    Use this instead when you would create a simple <table>
    ref. https://quasar.dev/vue-components/markup-table#qmarkuptable-api
    """
    component = 'q-markup-table'


class QMenu(ComponentWithModel):
    """
    QMenu is a popup, a dropdown or a normal menu (depending on its positioning).
    Its model controls the shown/hidden state.
    ref. https://quasar.dev/vue-components/menu#qmenu-api
    """
    component = 'q-menu'


class QResizeObserver(Component):
    """
    Calls event 'resize' if its parent element gets resized.
    Use 'debounce' prop to get a better performance.
    https://quasar.dev/vue-components/resize-observer#qresizeobserver-api
    """
    component = 'q-resize-observer'


class QScrollObserver(Component):
    """
    Calls event 'scroll' if its parent element gets resized.
    Use 'debounce' prop to get a better performance.
    https://quasar.dev/vue-components/scroll-observer#qscrollobserver-api
    """
    component = 'q-scroll-observer'


class QPagination(ComponentWithModel):
    """
    It shows the pagination buttons (but it does not do the pagination).
    prop 'max' is required
    https://quasar.dev/vue-components/pagination#qpagination-api
    """
    component = 'q-pagination'


class QParallax(Component):
    """
    https://quasar.dev/vue-components/parallax#qparallax-api
    """
    component = 'q-parallax'


class QPopupEdit(ComponentWithModel):
    """
    Use this to edit any value 'in-place'.
    It pops up an editor dialog.
    ref. https://quasar.dev/vue-components/popup-edit#qpopupedit-api
    """
    component = 'q-popup-edit'


class QPopupProxy(Component):
    """
    Creates a pop-up element.
    eg. InputDate, InputTime, InputDateTime uses it.
    ref. https://quasar.dev/vue-components/popup-proxy#qpopupproxy-api
    """
    component = 'q-popup-proxy'


class QPullToRefresh(Component):
    """
    This component is best used on mobile, it is not intuitive on desktops.
    Here it is defined merely for sake of completeness.
    It calls 'refresh' event when its parent gets dragged down (a pull).

    ref. https://quasar.dev/vue-components/pull-to-refresh#qpulltorefresh-api
    """
    component = 'q-pull-to-refresh'


class QRating(ComponentWithModel):
    """
    The classic star-rating.
    ref. https://quasar.dev/vue-components/rating#qrating-api
    """
    defaults = {
        'props': {
            'icon': 'star_border',
            'icon-selected': 'star'
        }
    }
    component = 'q-rating'


class QResponsive(Component):
    """
    Forces a responsively sized element to keep a pre-defined width to height ratio.
    props 'ratio' should be set.
    ref. https://quasar.dev/vue-components/responsive#qresponsive-api
    """
    component = 'q-responsive'


class QScrollArea(Component):
    """
    Makes a scrolled box with a squared scrollbar (by default).
    It can be fully customized (scrollbar and -area, direction, etc.).
    ref. https://quasar.dev/vue-components/scroll-area#qscrollarea-api
    """
    component = 'q-scroll-area'


class QSeparator(Component):
    """
    A horizontal or vertical line.
    prop inset: if True the line does not fully separate content.
    ref. https://quasar.dev/vue-components/separator
    """
    component = 'q-separator'


class QSkeleton(Component):
    """
    displays some placeholder gray shapes (prop: type) before the content arrives
    ref. https://quasar.dev/vue-components/skeleton#qskeleton-api
    """
    component = 'q-skeleton'


class QSlideItem(Component):
    """
    On mobile, list items can be usually slided left or right and some custom menu/action happens.
    This is the control for that. It works but it is not intuitive in a desktop environment.
    ref. https://quasar.dev/vue-components/slide-item#qslideitem-api
    """
    component = 'q-slide-item'


class QSlideTransition(Component):
    """
    It visually slides up or down a component if it gets shown/hidden.
    Usage:
    ::

        QSlideTransition([v_show(model_visible, QImg(src=src))])

    """
    component = 'q-slide-transition'


class QSpinner(Component):
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
                raise AssertionError('Appearance must be one of {}'.format(self.appearances))
            kwargs['component'] = 'q-spinner-{}'.format(appearance)
        super().__init__(**kwargs)


class QSplitter(Component):
    """
    Splits the area in two scrollable areas with a line inbetween,
    and the split line can be dragged by mouse.

    Works both horizontally and vertically.
    reference: https://quasar.dev/vue-components/splitter#qsplitter-api
    """
    component = 'q-splitter'


class QStepper(ComponentWithModel):
    """
    The classical wizzard,
    when the user needs to go through a multi-step process.
    ref. https://quasar.dev/vue-components/stepper#qstepper-api
    """
    component = 'q-stepper'

    def __init__(self,
                 model: Model = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: List[Union['QStep', Slot]] = None):
        super().__init__(model=model, classes=classes, styles=styles, props=props, events=events, children=children)


class QStep(Component):
    """
    Represents a step of a QStepper.
    ref. https://quasar.dev/vue-components/stepper#qstep-api
    """
    component = 'q-step'


class QStepperNavigation(Component):
    """
    Used in QStepper's 'navigation' Slot.
    ref. https://quasar.dev/vue-components/stepper#qsteppernavigation-api
    """
    component = 'q-stepper-navigation'


class QTable(Component):
    """
    A fully-featured table with sorting/filtering/pagination etc.
    Everything about it can be customized.

    Scoped slots are accessible with
    ::

        Slot('slot-name', lambda prop: [...children...])

    If interested in just a simple table, use QMarkupTable
    ref. https://quasar.dev/vue-components/table#qtable-api
    """
    component = 'q-table'


class QToolbar(Component):
    """
    reference: https://quasar.dev/vue-components/toolbar
    """
    component = 'q-toolbar'


class QTabs(ComponentWithModel):
    """
    ref. https://quasar.dev/vue-components/tabs#qtabs-api
    """
    component = 'q-tabs'

    def __init__(self,
                 model: Model,
                 children: List['QTab'] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        super().__init__(model=model, classes=classes, styles=styles, props=props, events=events, children=children)


class QTab(Component):
    """
    ref. https://quasar.dev/vue-components/tabs#qtab-api
    """
    component = 'q-tab'

    def __init__(self,
                 name: PropValueType[str] = None,
                 icon: PropValueType[str] = None,
                 label: PropValueType[str] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: ChildrenType = None):
        props = build_props({}, props, {
            'name': name,
            'icon': icon,
            'label': label
        })
        super().__init__(classes=classes, styles=styles, props=props, events=events, children=children)


# QRouteTab is not defined because we don't have router here.


class QTabPanels(ComponentWithModel):
    """
    The panels display for the QTabs.
    ref. https://quasar.dev/vue-components/tab-panels#qtabpanels-api
    """
    component = 'q-tab-panels'
    render_children_immediately = True

    def __init__(self,
                 model: Model,
                 children: List['QTabPanel'] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        super().__init__(model=model, classes=classes, styles=styles, props=props, events=events, children=children)


class QTabPanel(Component):
    """
    A panel in QTabPanels
    ref. https://quasar.dev/vue-components/tab-panels#qtabpanel-api
    """
    component = 'q-tab-panel'

    def __init__(self,
                 name: PropValueType[str],
                 children: ChildrenType = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None):
        props = build_props({}, props, {'name': name})
        super().__init__(classes=classes, styles=styles, props=props, events=events, children=children)


class QTimeline(Component):
    """
    Displays a timeline of events.
    ref. https://quasar.dev/vue-components/timeline#qtimeline-api
    """
    component = 'q-timeline'

    def __init__(self,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: List['QTimelineEntry'] = None):
        super().__init__(classes=classes, styles=styles, props=props, events=events, children=children)


class QTimelineEntry(Component):
    """
    An entry for QTimeline.
    ref. https://quasar.dev/vue-components/timeline#qtimelineentry-api
    """
    component = 'q-timeline-entry'


class QTooltip(Component):
    """
    Usage:
    ::

        QButton(children=['Submit', QTooltip(['Submit button'])])

    reference: https://quasar.dev/vue-components/tooltip
    """
    component = 'q-tooltip'


class QTree(Component):
    """
    reference: https://quasar.dev/vue-components/tree
    """
    component = 'q-tree'


class QUploader(Component):
    """
    This component uploads a file
    (Which is not really necessary in a desktop environment,
    since we usually have access to files by file path.
    If not, this QUploader component can be used.)
    ref. https://quasar.dev/vue-components/uploader#quploader-api
    """
    component = 'q-uploader'


class QVideo(Component):
    """
    ref. https://quasar.dev/vue-components/video#qvideo-api
    """
    component = 'q-video'

    def __init__(self,
                 src: PropValueType[str],
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 children: ChildrenType = None):
        props = build_props({}, props, {'src': src})
        super().__init__(classes=classes, styles=styles, props=props, events=events, children=children)


class QVirtualScroll(Component):
    """
    ref. https://quasar.dev/vue-components/virtual-scroll#qvirtualscroll-api
    """
    component = 'q-virtual-scroll'

    def __init__(self,
                 children: List[Slot] = None,
                 classes: ClassesType = None,
                 styles: StylesType = None,
                 props: PropsType = None,
                 events: EventsType = None,
                 ):
        super().__init__(
            children=children,
            classes=classes,
            styles=styles,
            props=props,
            events=events)
