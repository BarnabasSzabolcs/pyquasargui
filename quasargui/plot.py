import base64
from io import BytesIO
from os.path import join
from typing import TYPE_CHECKING

from quasargui import QUASAR_GUI_ASSETS_PATH
from quasargui.model import Model
from quasargui.base import Component
from quasargui.tools import str_between
from quasargui.typing import ClassesType, StylesType, PropValueType

try:
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    import mpld3 as mpld3
    MPLD3 = True
except ImportError:
    MPLD3 = False

try:
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    import matplotlib.pyplot as plt
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    import matplotlib
    # ref. https://stackoverflow.com/a/65793660/1031191
    matplotlib.use('Agg')  # if plt.subplots opens a window, this gui crashes, so we disable matplotlib gui.
    MATPLOTLIB = True
except ImportError:
    MATPLOTLIB = False

if TYPE_CHECKING:
    # noinspection PyPackageRequirements
    from matplotlib.pyplot import Figure


class Plot(Component):
    """
    This component is not a quasar component.
    If interactive=False, it can be styled, it shows a png image.
    However, if interactive=True, it can *not* be styled as it shows an interactive svg,
    created by mpld3.

    "Different sizes can be created using `plt.figure(figsize=(width,height))`
    where width and height are in inches."
    ref. https://stackoverflow.com/a/31843288/1031191

    TODO: Bokeh integration, probably via file_html
    ref. https://docs.bokeh.org/en/latest/docs/reference/embed.html#bokeh.embed.file_html
    otherwise a bokeh server needs to start in the background - which is also not impossible...
    """
    def __init__(self,
                 interactive: PropValueType[bool] = True,
                 classes: ClassesType = None,
                 styles: StylesType = None
                 ):
        self.interactive = Model(interactive) if isinstance(interactive, bool) else interactive
        self._check_imports()

        self.html = {}
        self.img_base64 = ''
        super().__init__(classes=classes, styles=styles)

    def _check_imports(self):
        if self.interactive.value:
            if not MPLD3:
                raise ImportError("Please install mpld3 package to use interactive plots")
        else:
            if not MATPLOTLIB:
                raise ImportError("Please install matplotlib package to use interactive plots")

    def set_figure(self, fig: 'Figure'):
        self.html = {}
        self.img_base64 = ''
        self._check_imports()
        if self.interactive.value:
            raw_html = mpld3.fig_to_html(
                fig,
                d3_url='file://' + join(QUASAR_GUI_ASSETS_PATH, 'd3.v5.js'),
                mpld3_url='file://' + join(QUASAR_GUI_ASSETS_PATH, 'mpld3.v0.5.2.js'),
            )
            self.html['figId'] = str_between(raw_html, '<div id="', '"></div>')
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
                'props': {
                    'script': self.html['script'],
                    'style': self.html['style'],
                    'figId': self.html['figId']
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
