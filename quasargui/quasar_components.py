from typing import List

from quasargui.base import Component, LabeledComponent, Model, Slot
from quasargui.tools import build_props
from quasargui.typing import ClassesType, StylesType, PropsType, PropValueType, EventsType, ChildrenType


class QBar(Component):
    """
    ref. https://quasar.dev/vue-components/bar#qbar-api
    """
    component = 'q-bar'


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


class QCard(Component):
    """
    ref. https://quasar.dev/vue-components/card#qcard-api
    Use it with QCardSection, QSeparator and QCardActions
    """
    component = 'q-card'


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


class QEditor(Component):
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
                 children: List[Slot] = None,
                 events: EventsType = None):
        model = model or Model('')
        props = props or {}
        props['v-model'] = model
        super().__init__(classes=classes, styles=styles, children=children, props=props, events=events)


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


class QItem(Component):
    component = 'q-item'


class QItemSection(Component):
    component = 'q-item-section'


class QList(Component):
    component = 'q-list'


class QMenu(Component):
    component = 'q-menu'


class QPopupProxy(Component):
    """
    Creates a pop-up element.
    eg. InputDate, InputTime, InputDateTime uses it.
    ref. https://quasar.dev/vue-components/popup-proxy#qpopupproxy-api
    """
    component = 'q-popup-proxy'


class QSeparator(Component):
    """
    A horizontal line.
    ref. https://quasar.dev/vue-components/separator
    """
    component = 'q-separator'


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
    reference: https://quasar.dev/vue-components/splitter
    """
    component = 'q-splitter'


class QToolbar(Component):
    """
    reference: https://quasar.dev/vue-components/toolbar
    """
    component = 'q-toolbar'


class QTooltip(Component):
    """
    reference: https://quasar.dev/vue-components/tooltip
    """
    component = 'q-tooltip'


class QTree(Component):
    """
    reference: https://quasar.dev/vue-components/tree
    """
    component = 'q-tree'
