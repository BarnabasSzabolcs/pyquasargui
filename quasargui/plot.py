import base64
from io import BytesIO
from os.path import join
from typing import TYPE_CHECKING

from quasargui import QUASAR_GUI_ASSETS_PATH
from quasargui.base import Component
from quasargui.model import Model
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

    "Different sizes can be created using ``plt.figure(figsize=(width,height))``
    where width and height are in inches."
    ref. https://stackoverflow.com/a/31843288/1031191

    TODO: Bokeh integration, probably via file_html
    ref. https://docs.bokeh.org/en/latest/docs/reference/embed.html#bokeh.embed.file_html
    otherwise a bokeh server needs to start in the background - which is also not impossible...
    """
    script_sources = ['mpld3-figure.js']
    defaults = {
        'render': 'png',  # other choice: 'mpld3'
    }
    renderers = {'png', 'mpld3'}

    def __init__(self,
                 renderer: PropValueType[str] = 'mpld3',
                 classes: ClassesType = None,
                 styles: StylesType = None
                 ):
        """
        :param renderer: valid values are 'png' and 'mpld3'.
        :param classes:
        :param styles:
        """
        self.renderer = Model(renderer) if isinstance(renderer, str) else renderer
        self.renderer.add_callback(self.update)
        self._check_imports()

        self.fig = None
        self.html = {}
        self.img_base64 = Model('')
        self.last_renderer = None
        super().__init__(classes=classes, styles=styles)
        self.dependents.append(self.img_base64)

    def _check_imports(self):
        if self.renderer.value == 'mpld3':
            if not MPLD3:
                raise ImportError("Please install mpld3 package to use interactive plots")
        elif self.renderer.value == 'png':
            if not MATPLOTLIB:
                raise ImportError("Please install matplotlib package to use interactive plots")
        else:
            raise AssertionError(
                'Wrong renderer. Renderer is set to "{wrong}", '
                'should be one of {should}'.format(
                    wrong=self.renderer.value, should=self.renderers
                ))

    def update(self):
        self.set_figure(self.fig)

    def set_figure(self, fig: 'Figure'):
        self.fig = fig
        self._check_imports()
        if self.renderer.value == 'mpld3':
            raw_html = mpld3.fig_to_html(
                fig,
                d3_url='file://' + join(QUASAR_GUI_ASSETS_PATH, 'd3.v5.js'),
                mpld3_url='file://' + join(QUASAR_GUI_ASSETS_PATH, 'mpld3.v0.5.2.js'),
            )
            self.html['figId'] = str_between(raw_html, '<div id="', '"></div>')
            self.html['script'] = str_between(raw_html, "<script>", "</script>")
            self.html['style'] = str_between(raw_html, "<style>", "</style>")
        elif self.renderer.value == 'png':
            tmpfile = BytesIO()
            fig.savefig(tmpfile, format='png')
            encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
            self.img_base64.value = "data:image/png;base64,{}".format(encoded)
        if self.last_renderer != self.renderer.value or self.renderer.value != 'png':
            super().update()
        self.last_renderer = self.renderer.value

    @property
    def vue(self) -> dict:
        if self.renderer.value == 'mpld3':
            return self._merge_vue({
                'component': 'mpld3-figure',
                'props': {
                    'script': self.html['script'],
                    'style': self.html['style'],
                    'figId': self.html['figId']
                }
            })
        elif self.renderer.value == 'png':
            return self._merge_vue({
                'component': 'img',
                'props': {'src': self.img_base64.render_as_data()}
            })
        else:
            return self._merge_vue({
                'component': 'div'
            })
