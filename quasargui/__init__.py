__version__ = '0.1'

from os.path import join, dirname

this_directory = dirname(__file__)
QUASAR_GUI_ASSETS_PATH = join(this_directory, 'assets')
QUASAR_GUI_INDEX_PATH = join(QUASAR_GUI_ASSETS_PATH, 'index.html')

from .main import run, set_main_component
from ._base import Model
