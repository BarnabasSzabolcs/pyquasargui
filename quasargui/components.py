# noinspection PyUnresolvedReferences
import base64
from io import BytesIO
from typing import TYPE_CHECKING

try:
    # noinspection PyPackageRequirements
    import mpld3 as mpld3
    MPLD3 = True
except ImportError:
    MPLD3 = False

try:
    # noinspection PyPackageRequirements
    import matplotlib.pyplot as plt
    import matplotlib
    # ref. https://stackoverflow.com/a/65793660/1031191
    matplotlib.use('Agg')  # if plt.subplots opens a window, this gui crashes, so we disable matplotlib gui.
    MATPLOTLIB = True
except ImportError:
    MATPLOTLIB = False

from ._base import Component
# noinspection PyUnresolvedReferences
from ._form import Button, Input
# noinspection PyUnresolvedReferences
from ._layout import Layout, Header, Drawer, Page, Footer, Toolbar, ToolbarTitle, Icon, Space
from ._tools import merge_classes, str_between
from .typing import *

if TYPE_CHECKING:
    from matplotlib.figure import Figure


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


class Plot(Component):
    def __init__(self,
                 interactive: bool = True,
                 classes: ClassesType = None,
                 styles: StylesType = None
                 ):
        self.interactive = interactive
        if interactive:
            if not MPLD3:
                raise ImportError("Please install mpld3 package to use interactive plots")
        else:
            if not MATPLOTLIB:
                raise ImportError("Please install matplotlib package to use interactive plots")

        self.html = {}
        self.img_base64 = ''
        super().__init__(classes=classes, styles=styles)

    def set_figure(self, fig: 'Figure', ax):
        self.html = {}
        self.img_base64 = ''
        if self.interactive:
            raw_html = mpld3.fig_to_html(fig)
            self.html['div'] = str_between(raw_html, "<div>", "</div>")
            self.html['script'] = str_between(raw_html, "<script>", "</script>")
            self.html['style'] = str_between(raw_html, "<style>", "</style>")
        else:
            tmpfile = BytesIO()
            fig.savefig(tmpfile, format='png')
            encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
            self.img_base64 = "data:image/png;base64,{}".format(encoded)
        self.update()

    @property
    def vue(self) -> dict:
        if self.html:
            return self._merge_vue({
                'component': 'mpld3-figure',
                'children': [self.html['div']],
                'props': {
                    'script': self.html['script'],
                    'style': self.html['style']
                }
            })
        elif self.img_base64:
            return self._merge_vue({
                'component': 'q-img',
                'props': {'src': self.img_base64}
            })
        else:
            return self._merge_vue({
                'component': 'div'
            })
