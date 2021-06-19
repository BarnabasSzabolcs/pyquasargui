__version__ = '0.1'

from os.path import join, dirname

this_directory = dirname(__file__)
QUASAR_GUI_ASSETS_PATH = join(this_directory, 'assets')
QUASAR_GUI_INDEX_PATH = join(QUASAR_GUI_ASSETS_PATH, 'index.html')

from quasargui.main import run, set_main_component
from quasargui.base import *
from quasargui.callbacks import *
from quasargui.components import *
from quasargui.quasar_components import *
from quasargui.quasar_form import *
from quasargui.quasar_form_improved import *
from quasargui.layout import *
from quasargui.model import *
from quasargui.quasar_plugins import *
